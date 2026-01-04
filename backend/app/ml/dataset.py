import os
from pathlib import Path
from typing import Callable, List
from PIL import Image
import numpy as np
import torch
from torch.utils.data import Dataset
import albumentations as A

class SegmentationDataset(Dataset):
    def __init__(self, image_paths: List[Path], mask_paths: List[Path], transforms: Callable=None):
        self.images = image_paths
        self.masks = mask_paths
        self.transforms = transforms
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img = np.array(Image.open(self.images[idx]).convert("RGB"))
        mask = np.array(Image.open(self.masks[idx]).convert("L"))
        if self.transforms:
            aug = self.transforms(image = img, mask = mask)
            img, mask = aug["image"], aug["mask"]
        img = torch.from_numpy(img).permute(2,0,1).float()/255.0
        mask = torch.from_numpy((mask>127).astype("float32")).unsqueeze(0)
        return img, mask