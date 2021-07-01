def clone(module, n):
    return nn.ModuleList([deepcopy(module) for _ in range(n)])

class EncoderDecoder(nn.Module):
    def __init__(self, encoder, decoder):
        super(EncoderDecoder, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
    def forward(self, src, tgt, src_mask, tgt_mask):
        return self.decoder(encoder(src, src_mask), tgt, src_mask, tgt_mask)

class Encoder(nn.Module):
    def __init__(self, encoder_layer, n=6):
        super(Encoder, self).__init__()
        self.layers = clone(encoder_layer, n)
    def forward(self, src, src_mask):
        x = f(src, src_mask)
        for l in self.layers:
            x = l(x)
        return x

class EncoderLayer(nn.Module):
    def __init__(self, ff, attn):
        super(EncoderLayer, self).__init__():
        self.sublayers = clone(sublayer, 2)
        self.ff = ff
        self.attn = attn
    def forward(self, x):
        return self.sublayers[1](self.ff, self.sublayers[0](
            lambda x: self.attn(x, x, x), x))

class SubLayer(nn.Module):
    def __init__(self, size, dropout):
        super(SubLayer, self).__init__()
        self.norm = LayerNorm(size)
        self.dropout = nn.Dropout(dropout)
    def forward(self, module, x):
        return x + self.dropout(module(self.norm(x)))

def attention(query, key, value, mask=None, dropout=None):
    score = torch.matmul(query, key.transpose(-2, -1)) / sqrt(query.size(-1)
    if mask:
        score = score.masked_fill(mask==0, -1e9)
    p_attn = F.softmax(score, dim=-1)
    if dropout:
        p_attn = dropout(p_attn)
    return torch.matmul(p_attn, value), p_attn

class MultiHeadAttention(nn.Module):
    def __init__(self, h, d_model):
        super(MultiHeadAttention, self).__init__()
        self.linears = nn.ModuleList([nn.Linear(d_model, d_model) for
            _ in range(4)])
        self.h = h
        self.d_k = d_model // h
    def forward(self, q, k, v):
        nbatches = q.size(0)
        q, k, v = [l(x).view(nbatches, -1, self.h, self.d_k).transpose(-2,
            -3) for (l, x) in zip(self.linears[:3], (q, k, v))]
        attn, p_attn = attention(q, k, v)
        attn = attn.transpose(-2, -3).view(nbatches, -1, d_model
            ).contiguous()
        return self.linears[-1](attn)

class Decoder(nn.Module):
    def __init__(self, n, decoder_layer):
        super(Decoder, self).__init__()
        self.layers = clone(decoder_layer, n)
    def forward(self, mmr, tgt, src_mask, tgt_mask):
        for l in self.layers:
            x = l(x, mmr)
        return x

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













