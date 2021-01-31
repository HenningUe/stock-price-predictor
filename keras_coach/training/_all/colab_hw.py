
import os
import tensorflow as tf
import enum
# sources
# https://colab.research.google.com/github/tensorflow/tpu/blob/master/tools/colab/classification_iris_data_with_keras.ipynb#scrollTo=ZbwW0pDxFQyx
#
# outdated
#     [https://blog.tensorflow.org/2019/01/keras-on-tpus-in-colab.html]
#     [https://www.dlology.com/blog/how-to-train-keras-model-x20-times-faster-with-tpu-for-free/]

# GPU
# https://www.tutorialspoint.com/google_colab/google_colab_using_free_gpu.htm

shall_run_on_tpu = False


class HwSupportType(enum.IntEnum):
    none = 0
    gpu = 1
    tpu = 2


def get_hw_support_type():
    gpu_device_name = get_gpu_device_name()
    if gpu_device_name is not None:
        return HwSupportType.gpu
    elif is_to_be_run_on_tpu():
        return HwSupportType.tpu
    else:
        return HwSupportType.none


def get_gpu_device_name():
    device_name = tf.test.gpu_device_name()
    if device_name is None or len(device_name) == 0:
        device_name = None
    return device_name


def is_to_be_run_on_tpu():
    global shall_run_on_tpu
    return (shall_run_on_tpu is True
            and get_tpu_address() is not None)


def get_tpu_address():
    try:
        device_name = os.environ['COLAB_TPU_ADDR']
        tpu_address = 'grpc://' + device_name
        return tpu_address
    except KeyError:
        return None
