# -*- coding: utf-8 -*-

import os
import shutil
import argparse
from tqdm import tqdm

import gym
from gym.wrappers.atari_preprocessing import AtariPreprocessing
from gym.wrappers.frame_stack import FrameStack

import cv2
import numpy as np
import paddle.fluid as fluid


def imgs2video(imgs_dir, save_name):
    img_root = imgs_dir
    fps = 24

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videoWriter = cv2.VideoWriter(save_name, fourcc, fps, (160, 210))  # 最后一个是保存图片的尺寸

    image_list = os.listdir(imgs_dir)
    image_list = [x for x in image_list if not x.startswith('.')]

    for i in range(len(image_list)):
        frame = cv2.imread(os.path.join(img_root, str(i)) + '.jpg')
        videoWriter.write(frame)
    videoWriter.release()
    shutil.rmtree(img_root)


def batch_img2video(dir_path):
    mulu_list = os.listdir(dir_path)
    mulu_list = [x for x in mulu_list if not x.startswith('.')]
    for i in mulu_list:
        if os.path.isdir(os.path.join(dir_path, i)):
            imgs2video(os.path.join(dir_path, i), os.path.join(dir_path, i) + ".avi")


def predict_action(exe, state, predict_program, feed_names, fetch_targets,
                   action_dim):
    if np.random.random() < 0.01:
        act = np.random.randint(action_dim)
    else:
        state = np.expand_dims(state, axis=0)
        pred_Q = exe.run(predict_program,
                         feed={feed_names[0]: state.astype('float32')},
                         fetch_list=fetch_targets)[0]
        pred_Q = np.squeeze(pred_Q, axis=0)
        act = np.argmax(pred_Q)
    return act

def get_env(env_name):
    env = gym.make(env_name)
    env = AtariPreprocessing(env)
    env = FrameStack(env, 4)
    return env


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--use_cuda', action='store_true', help='if set, use cuda')
    parser.add_argument('--game', type=str, required=True, help='atari rom')
    parser.add_argument(
        '--model_path', type=str, required=True, help='dirname to load model')
    parser.add_argument(
        '--viz', action='store_true', help='if set, generate videos.')
    args = parser.parse_args()

    if not os.path.isdir("videos"):
        os.mkdir("videos")

    env = get_env(args.game)

    place = fluid.CUDAPlace(0) if args.use_cuda else fluid.CPUPlace()
    exe = fluid.Executor(place)
    inference_scope = fluid.Scope()
    with fluid.scope_guard(inference_scope):
        [predict_program, feed_names,
         fetch_targets] = fluid.io.load_inference_model(args.model_path, exe)

        episode_reward = []
        for idx in tqdm(range(1, 2), desc='eval agent'):
            frames = 1
            total_reward = 0
            if args.viz:
                if not os.path.isdir("videos/{}".format(str(idx))):
                    os.mkdir("videos/{}".format(str(idx)))
            state = env.reset()
            while True:
                if args.viz:
                    image = env.unwrapped.render('rgb_array')
                    cv2.imwrite("videos/{}/{}.jpg".format(str(idx), str(frames)), image)
                    frames += 1
                action = predict_action(exe, state, predict_program, feed_names,
                                        fetch_targets, env.action_space.n)
                state, reward, isOver, info = env.step(action)
                total_reward += reward
                if isOver:
                    break
            episode_reward.append(total_reward)
        eval_reward = np.mean(episode_reward)
        print('Average reward of epidose: {}'.format(eval_reward))
    batch_img2video("videos")
