import torch
import torch.nn as nn
import math
from copy import deepcopy

# Helper function to duplicate layers
def clone(module, n):
    return nn.ModuleList([deepcopy(module) for _ in range(n)])

# The transformer is an encoder-decoder architecture
class Transformer(nn.Module):
    def __init__(self, encoder, decoder):
        super(Transformer, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
    def forward(self, src, tgt, src_mask, tgt_mask):
        return self.decoder(encoder(src, src_mask), tgt, src_mask, tgt_mask)

# The encoder is a multi-layer structure 
class Encoder(nn.Module):
    def __init__(self, encoder_layer, n=6):
        super(Encoder, self).__init__()
        self.layers = clone(encoder_layer, n)
    def forward(self, src, src_mask):
        x = src
        for l in self.layers:
            x = l(x, src_mask)
        return x

# Each encoder layer contains a multi-head attention layer
# and a feed forward layer
class EncoderLayer(nn.Module):
    def __init__(self, ff, attn):
        super(EncoderLayer, self).__init__():
        self.sublayers = clone(sublayer, 2)
        self.ff = ff
        self.attn = attn
    def forward(self, x, src_mask):
        return self.sublayers[1](self.ff, self.sublayers[0](
            lambda x: self.attn(x, x, x), x))

# Dropout, layer normalization and residual connection are applied
# in each sublayer
class SubLayer(nn.Module):
    def __init__(self, d_model, dropout):
        super(SubLayer, self).__init__()
        self.norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    def forward(self, f, x):
        return x + self.dropout(f(self.norm(x)))

# Attention mechanism
def attention(query, key, value, mask=None, dropout=None):
    score = torch.matmul(query, key.transpose(-2, -1)) / sqrt(query.size(-1)
    if mask:
        score += mask
    score = F.softmax(score, dim=-1)
    if dropout:
        score = dropout(score)
    return torch.matmul(score, value), score

# Multihead attention layer
class MultiHeadAttention(nn.Module):
    def __init__(self, h, d_model):
        super(MultiHeadAttention, self).__init__()
        self.linears = nn.ModuleList([nn.Linear(d_model, d_model) for
            _ in range(4)])
        self.h = h
        self.d_k = d_model // h
    def forward(self, q, k, v):
        num_batches = q.size(0)
        # Original shape of q, k, v: [num_batches, length, d_model]
        # New shape: [num_batches, h, length, d_model/h]
        q, k, v = [l(x).view(num_batches, -1, self.h, self.d_k).transpose(-2,
                -3) for (l, x) in zip(self.linears[:3], (q, k, v))]
        attn, score = attention(q, k, v)
        attn = attn.transpose(-2, -3).view(num_batches, -1, d_model)\
                .contiguous()
        return self.linears[-1](attn)

# The decoder is also a multi-layer structure similar to the encoder
class Decoder(nn.Module):
    def __init__(self, n, decoder_layer):
        super(Decoder, self).__init__()
        self.layers = clone(decoder_layer, n)
    def forward(self, mmr, tgt, src_mask, tgt_mask):
        for l in self.layers:
            x = l(x, mmr)
        return x

# Each decoder layer contains a self-attention layer, a multi-head
# attention layer and a feed-forward layer
class DecoderLayer(nn.Module):
    def __init__(self, self_attn, src_attn, ff):
        super(DecoderLayer, self).__init__()
        self.sublayers = clone(sublayer, 3)
        self.self_attn = self_attn
        self.src_attn = src_attn
        self.ff = ff
    def forward(self, x, mmr)
        l = self.sublayers
        x = l[0](lambda x: self.self_attn(x, x, x), x)
        x = l[1](lambda x: src_attn(x, mmr, mmr), x)
        x = l[2](ff, x)
        return x

# Positional encoding
def pe(length, d_model):
    pos = torch.arange(length).unsqueeze(dim=1)
    div = torch.exp(-torch.arange(0, d_model, 2, dtype=torch.float) *\
            math.log(10000) / d_model)
    pe = torch.zeros(length, d_model)
    pe[::2] = torch.sin(pos * div)
    pe[1::2] = torch.cos(pos * div)










