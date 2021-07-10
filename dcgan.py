import argparse
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision.transforms as T
import torchvision.utils as vutils
from torch.utils.data import DataLoader

# Hyperparameters
lr = .0002
beta1 = .5
b_size = 64
num_epochs = 5
nz = 100
nf = 64
nc = 3

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

data = datasets.CelebA('.', transform=T.Compose([T.ReSize(64),
                                                 T.CenterCrop(64),
                                                 T.ToTensor(),
                                                 T.Normalize(.5, .5)
                                      ])
)

loader = DataLoader(data, batch_size=b_size, shuffle=True)

G = nn.Sequential(
    # nz * 1 * 1
    nn.ConvTranspose2d(nz, 8*nf, 4, bias=False)
    nn.BatchNorm2d(8*nf)
    nn.ReLU(True)
    # 8nf * 4 * 4
    nn.ConvTranspose2d(8*nf, 4*nf, 4, 2, 1, bias=False)
    nn.BatchNorm2d(4*nf)
    nn.ReLU(True)
    # 4nf * 8 * 8
    nn.ConvTranspose2d(4*nf, 2*nf, 4, 2, 1, bias=False)
    nn.BatchNorm2d(2*nf)
    nn.ReLU(True)
    # 2nf * 16 * 16
    nn.ConvTranspose2d(2*nf, nf, 4, 2, 1, bias=False)
    nn.BatchNorm2d(nf)
    nn.ReLU(True)
    # nf * 32 * 32
    nn.ConvTranspose2d(nf, nc, 4, 2, 1, bias=False)
    nn.tanh()
    # 3 * 64 * 64
)

D = nn.Sequential(
    # 3 * 64 * 64
    nn.Conv2d(3, nf, 4, 2, 1, bias=False)
    nn.LeakyReLU(.2, True)
    # nf * 32 * 32
    nn.Conv2d(nf, 2*nf, 4, 2, 1, bias=False)
    nn.BatchNorm2d(2*nf)
    nn.LeakyReLU(.2, True)
    # 2nf * 16 * 16
    nn.Conv2d(2*nf, 4*nf, 4, 2, 1, bias=False)
    nn.BatchNorm2d(4*nf)
    nn.LeakyReLU(.2, True)
    # 4nf * 8 * 8
    nn.Conv2d(4*nf, 8*nf, 4, 2, 1, bias=False)
    nn.BatchNorm2d(8*nf)
    nn.LeakyReLU(.2, True)
    # 8nf * 4 * 4
    nn.Conv2d(8*nf, 1, 4, bias=False)
    # 1 * 1 * 1
)

def init_params(m):
    if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d):
        m.weight.data.normal_(0, .02)
    if isinstance(m, nn.BatchNorm2d):
        m.weight.data.normal_(1., .02)

G.apply(init_params)
D.apply(init_params)

G.to(device)
D.to(device)

opt_g = optim.Adam(G.parameters(), lr=lr, betas=(beta1, .999))
opt_d = optim.Adam(D.parameters(), lr=lr, betas=(beta1, .999))

criterion = nn.BCEWithLogitsLoss()

z_fixed = torch.randn(b_size, nz, 1, 1, device=device)

i = 0
e = 0
acc_loss = 0
min_loss = float('inf')
samples = []

while True:
    e += 1
    if e > num_epochs:
        break
    for real in data:
        i += 1
        real = real.to(device)
        z = torch.randn(real.shape[0], nz, 1, 1, device=device)
        ones = torch.ones(real.shape[0], device=device)
        zeros = torch.zeros(real.shape[0], device=device)
        # D update
        loss_real = criterion(D(real).view(-1), ones)
        opt_d.zero_grad()
        loss_real.backward()
        loss_fake = criterion(D(G(z).detach()).view(-1), zeros)
        loss_fake.backward()
        opt_d.step()
        loss_d = (loss_real + loss_fake) / 2
        # G update
        opt_g.zero_grad()
        loss_g = criterion(D(G(z)).view(-1), ones)
        loss_g.backward()
        opt_g.step()
        acc_loss += loss_g.item()
    # Checkpointing
    if not i % 100:
        # Early stopping
        if acc_loss >= min_loss:
            break
        acc_loss, min_loss = 0, acc_loss
        with torch.no_grad():
            sample = G(z_fixed)
            samples.append(vutils.make_grid(sample, normalize=True).cpu()\
                    .numpy())


