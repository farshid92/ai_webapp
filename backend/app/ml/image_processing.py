"""
Image Processing Utilities for Computer Vision Tasks

Handles image preprocessing, post-processing, and visualization for segmentation.
"""

import numpy as np
import torch
from PIL import Image
import io
import base64
from typing import Tuple, Optional
import cv2


def preprocess_image(
    image: Image.Image,
    target_size: Tuple[int, int] = (256, 256),
    normalize: bool = True
) -> torch.Tensor:
    """
    Preprocess image for model input
    
    Args:
        image: PIL Image
        target_size: Target (height, width)
        normalize: Whether to normalize to [0, 1]
        
    Returns:
        Preprocessed tensor of shape (1, C, H, W)
    """
    # Resize
    image = image.resize(target_size, Image.Resampling.BILINEAR)
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Handle different image formats
    if len(img_array.shape) == 2:  # Grayscale
        img_array = np.expand_dims(img_array, axis=2)
    
    # Convert RGB to BGR if needed (OpenCV format)
    if img_array.shape[2] == 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    
    # Normalize
    if normalize:
        img_array = img_array.astype(np.float32) / 255.0
    
    # Convert to tensor: (H, W, C) -> (C, H, W)
    img_tensor = torch.from_numpy(img_array).permute(2, 0, 1).float()
    
    # Add batch dimension: (C, H, W) -> (1, C, H, W)
    img_tensor = img_tensor.unsqueeze(0)
    
    return img_tensor


def postprocess_mask(
    mask: torch.Tensor,
    original_size: Tuple[int, int],
    threshold: float = 0.5
) -> np.ndarray:
    """
    Postprocess segmentation mask
    
    Args:
        mask: Model output tensor
        original_size: Original image size (height, width)
        threshold: Threshold for binary mask
        
    Returns:
        Postprocessed mask as numpy array
    """
    # Remove batch dimension if present
    if mask.dim() == 4:
        mask = mask.squeeze(0)
    
    # Apply sigmoid if needed (for single channel)
    if mask.shape[0] == 1:
        mask = torch.sigmoid(mask)
        mask = (mask > threshold).float()
    
    # Convert to numpy
    mask_np = mask.squeeze(0).cpu().numpy()
    
    # Resize to original size
    mask_np = cv2.resize(
        mask_np,
        (original_size[1], original_size[0]),
        interpolation=cv2.INTER_NEAREST
    )
    
    return (mask_np * 255).astype(np.uint8)


def overlay_mask_on_image(
    image: Image.Image,
    mask: np.ndarray,
    alpha: float = 0.5,
    color: Tuple[int, int, int] = (255, 0, 0)
) -> Image.Image:
    """
    Overlay segmentation mask on original image
    
    Args:
        image: Original PIL Image
        mask: Segmentation mask (numpy array)
        alpha: Transparency of overlay
        color: Color for mask overlay (R, G, B)
        
    Returns:
        PIL Image with overlay
    """
    # Convert image to numpy
    img_array = np.array(image)
    
    # Create colored mask
    colored_mask = np.zeros_like(img_array)
    mask_binary = mask > 128
    
    for i in range(3):
        colored_mask[:, :, i] = mask_binary * color[i]
    
    # Blend
    overlay = (alpha * colored_mask + (1 - alpha) * img_array).astype(np.uint8)
    
    return Image.fromarray(overlay)


def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/{format.lower()};base64,{img_str}"


def base64_to_image(base64_str: str) -> Image.Image:
    """Convert base64 string to PIL Image"""
    # Remove data URL prefix if present
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]
    
    img_data = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(img_data))


