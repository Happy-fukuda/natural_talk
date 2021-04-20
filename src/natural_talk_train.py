# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow import keras
import numpy as np
import sys
import time

sys.path.append('..')
from common import data_operation , Attention_Model

data_class=data_operation.DataOperation()
(input_train,input_test) , (output_train , output_test) = data_class.data_load()
targ_lang=data_class.get_size()

BUFFER_SIZE = len(input_train)
BATCH_SIZE = 64
steps_per_epoch = len(input_train)//BATCH_SIZE
embedding_dim = 256
units = 1024
#このデータを何回学習させるか
EPOCHS = 10
#encoderとdecorderを定義
encoder = Encoder(vocab_inp_size, embedding_dim, units, BATCH_SIZE)
decoder = Decoder(vocab_tar_size, embedding_dim, units, BATCH_SIZE)
#使う最適化アルゴリズムと損失関数を定義
optimizer = tf.keras.optimizers.Adam()
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=True, reduction='none')

#保存するための変数を定義
checkpoint_dir = './training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(optimizer=optimizer,
                                 encoder=encoder,
                                 decoder=decoder)


#損失関数とオプティマイザ
def loss_function(real, pred):
    mask = tf.math.logical_not(tf.math.equal(real, 0)) #equal:real==0の真理値 logical_not : 真理値の逆を返す
    loss_ = loss_object(real, pred)    # 交差エントロピー誤差

    mask = tf.cast(mask, dtype=loss_.dtype)  #
    loss_ *= mask

    return tf.reduce_mean(loss_)


def train_step(inp, targ, enc_hidden):
    loss = 0

    with tf.GradientTape() as tape:
        enc_output, enc_hidden = encoder(inp, enc_hidden)

        dec_hidden = enc_hidden

        dec_input = tf.expand_dims([targ_lang['<start>']] * BATCH_SIZE, 1)

        # Teacher Forcing - 正解値を次の入力として供給
        for t in range(1, targ.shape[1]):
            # passing enc_output to the decoder
            predictions, dec_hidden, _ = decoder(dec_input, dec_hidden, enc_output)

            loss += loss_function(targ[:, t], predictions)

            # Teacher Forcing を使用
            dec_input = tf.expand_dims(targ[:, t], 1)

    batch_loss = (loss / int(targ.shape[1]))

    variables = encoder.trainable_variables + decoder.trainable_variables

    gradients = tape.gradient(loss, variables)

    optimizer.apply_gradients(zip(gradients, variables))　#adam

    return batch_loss


if __name__=="__main__":
    for epoch in range(EPOCHS):
        start = time.time()

        enc_hidden = encoder.initialize_hidden_state()
        total_loss = 0

        for (batch, (inp, targ)) in enumerate(dataset.take(steps_per_epoch)):
            batch_loss = train_step(inp, targ, enc_hidden)
            total_loss += batch_loss

            if batch % 100 == 0:
                print('Epoch {} Batch {} Loss {:.4f}'.format(epoch + 1,
                                                         batch,
                                                         batch_loss.numpy()))
      # 2 エポックごとにモデル（のチェックポイント）を保存
        if (epoch + 1) % 2 == 0:
            checkpoint.save(file_prefix = checkpoint_prefix)

        print('Epoch {} Loss {:.4f}'.format(epoch + 1,
                                          total_loss / steps_per_epoch))
        print('Time taken for 1 epoch {} sec\n'.format(time.time() - start))
