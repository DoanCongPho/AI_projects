# SVD Image Compression

Truncated singular value decomposition keeps only the strongest features of an
image and rebuilds the picture from them.

Everything lives in one notebook: **`svd_image_compression.ipynb`**.

## The idea

Every channel of an image is a matrix `A` of size `m x n`. Its SVD is

```
A = U S V^T = sum_i  sigma_i * u_i * v_i^T
```

with `sigma_1 >= sigma_2 >= ... >= 0`. Cutting the sum off after `k` terms gives
`A_k`, which the Eckart-Young theorem says is the best possible rank-k
approximation in Frobenius norm. Each `sigma_i^2` is the energy that layer
carries, so a spectrum that decays fast means a few layers hold almost the whole
picture.

Storage drops from `m*n` numbers per channel to `k*(m + n + 1)`: the first `k`
columns of `U`, the first `k` singular values, and the first `k` rows of `V^T`.
Compression pays off whenever `k < m*n / (m + n + 1)`.

## Run it

Open the notebook and run section 0. It installs `numpy`, `pillow`, and
`matplotlib` into whichever kernel is executing the notebook, so with conda they
land in the active environment rather than in `base`. Nothing to install by hand
first, and no separate requirements file to keep in sync.

The notebook ships already executed, so every figure is visible without running a
cell. To use your own picture, change `IMAGE_PATH` in the setup cell and re-run.
`load_image(IMAGE_PATH, gray=True)` switches to a single channel.

## What it covers

| Section | Contents |
| --- | --- |
| 0 | install and report the three libraries it needs |
| 1-2 | setup, load the image, scale pixels to `[0, 1]` |
| 3 | thin SVD of every colour channel |
| 4 | singular value spectrum and cumulative energy |
| 5 | rank-k reconstruction, grid of every rank beside the original |
| 6 | compression ratio, PSNR, break-even rank |
| 7 | chosen reconstruction plus an absolute-error map |
| 8 | save the truncated factors, load them back, check the round trip |
| 9 | caveat on file size, exercises |

Figures and the compressed `.npz` are written to `output_notebook/`.

## A caveat on file size

The `.npz` factors are raw numbers with no entropy coding, so on disk they are
usually larger than the same image as PNG or JPEG. SVD compresses the *matrix
rank*, not the byte stream. Read the `stored` and `ratio` columns for the real
result, and treat the `.npz` size as a curiosity.
