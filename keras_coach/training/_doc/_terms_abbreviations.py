# -*- coding: utf-8 -*-

""""
======================
batch_size

https://stats.stackexchange.com/questions/153531/what-is-batch-size-in-neural-network

The batch size defines the number of samples that will be propagated through the network.
For instance, let's say you have 1050 training samples and you want to set up a batch_size equal to 100. The algorithm
takes the first 100 samples (from 1st to 100th) from the training dataset and trains the network.
Next, it takes the second 100 samples (from 101st to 200th) and trains the network again.
We can keep doing this procedure until we have propagated all samples through of the network.
Problem might happen with the last set of samples. In our example, we've used 1050 which is not
divisible by 100 without remainder. The simplest solution is just to get the final 50 samples and train the network.

Advantages of using a batch size < number of all samples:
    It requires less memory. Since you train the network using fewer samples, the overall training procedure requires
    less memory. That's especially important if you are not able to fit the whole dataset in your machine's memory.

    Typically networks train faster with mini-batches. That's because we update the weights after each propagation.
    In our example we've propagated 11 batches (10 of them had 100 samples and 1 had 50 samples) and after
    each of them we've updated our network's parameters. If we used all samples during propagation we
    would make only 1 update for the network's parameter.

Disadvantages of using a batch size < number of all samples:
    The smaller the batch the less accurate the estimate of the gradient will be.
    In the figure below, you can see that the direction of the mini-batch gradient (green color)
    fluctuates much more in comparison to the direction of the full batch gradient (blue color).


======================
epoch, batch_size, iteration

one epoch = one forward pass and one backward pass of all the training examples
batch size = the number of training examples in one forward/backward pass. The higher the batch size,
             the more memory space you'll need.
number of iterations = number of passes, each pass using [batch size] number of examples. To be clear,
                       one pass = one forward pass + one backward pass (we do not count the forward
                       pass and backward pass as two different passes).

Example: if you have 1000 training examples, and your batch size is 500, then it will take
2 iterations to complete 1 epoch.


"""
