"""
Image Segmentation API Endpoints

Handles image upload, segmentation, and visualization.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import torch
from app.ml.unet import UNet
from app.ml.loader import DEVICE
from app.ml.image_processing import (
    preprocess_image,
    postprocess_mask,
    overlay_mask_on_image,
    image_to_base64
)
from app.ml.registry import get_model
import io

router = APIRouter(prefix="/segmentation", tags=["segmentation"])


@router.post("/predict")
async def segment_image(
    file: UploadFile = File(...),
    model_name: str = "unet",
    threshold: float = 0.5,
    overlay: bool = True
):
    """
    Segment an uploaded image using U-Net
    
    Args:
        file: Uploaded image file
        model_name: Name of the model to use
        threshold: Threshold for binary mask
        overlay: Whether to return overlay visualization
        
    Returns:
        JSON with segmentation results
    """
    try:
        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        original_size = image.size[::-1]  # (width, height) -> (height, width)
        
        # Preprocess
        img_tensor = preprocess_image(image, target_size=(256, 256))
        img_tensor = img_tensor.to(DEVICE)
        
        # Get model (for now, create U-Net if not in registry)
        try:
            model = get_model(model_name)
        except KeyError:
            # Create default U-Net if not in registry
            model = UNet(in_channels=3, out_channels=1)
            model.to(DEVICE)
            model.eval()
        
        # Predict
        with torch.no_grad():
            mask_logits = model.predict(img_tensor)
        
        # Postprocess
        mask = postprocess_mask(mask_logits, original_size, threshold)
        
        # Prepare response
        response = {
            "success": True,
            "original_size": {"width": original_size[1], "height": original_size[0]},
            "mask_size": {"width": mask.shape[1], "height": mask.shape[0]}
        }
        
        # Convert mask to image
        mask_image = Image.fromarray(mask, mode="L")
        response["mask"] = image_to_base64(mask_image)
        
        # Add overlay if requested
        if overlay:
            overlay_img = overlay_mask_on_image(image, mask, alpha=0.5)
            response["overlay"] = image_to_base64(overlay_img)
        
        return JSONResponse(content=response)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Segmentation failed: {str(e)}"
        )


@router.post("/batch")
async def segment_batch(
    files: list[UploadFile] = File(...),
    model_name: str = "unet",
    threshold: float = 0.5
):
    """
    Segment multiple images in batch
    
    Args:
        files: List of uploaded image files
        model_name: Name of the model to use
        threshold: Threshold for binary mask
        
    Returns:
        List of segmentation results
    """
    results = []
    
    for file in files:
        try:
            # Read image
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            original_size = image.size[::-1]
            
            # Preprocess
            img_tensor = preprocess_image(image, target_size=(256, 256))
            img_tensor = img_tensor.to(DEVICE)
            
            # Get model
            try:
                model = get_model(model_name)
            except KeyError:
                model = UNet(in_channels=3, out_channels=1)
                model.to(DEVICE)
                model.eval()
            
            # Predict
            with torch.no_grad():
                mask_logits = model.predict(img_tensor)
            
            # Postprocess
            mask = postprocess_mask(mask_logits, original_size, threshold)
            mask_image = Image.fromarray(mask, mode="L")
            
            results.append({
                "filename": file.filename,
                "success": True,
                "mask": image_to_base64(mask_image)
            })
        
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return {"results": results}


