import torch
import torch.nn as nn
import torch.nn.functional as F


class DoubleConv(nn.Module):
    """Double convolution block: Conv -> BN -> ReLU -> Conv -> BN -> ReLU"""
    
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.double_conv(x)


class UNet(nn.Module):
    """
    U-Net Architecture for Semantic Image Segmentation
    
    Architecture:
    - Encoder (downsampling path): Captures context
    - Decoder (upsampling path): Enables precise localization
    - Skip connections: Preserves fine-grained details
    """
    
    def __init__(
        self,
        in_channels: int = 3,
        out_channels: int = 1,
        features: list[int] = [64, 128, 256, 512]
    ):
        """
        Args:
            in_channels: Number of input channels (1 for grayscale, 3 for RGB)
            out_channels: Number of output classes/channels
            features: List of feature sizes for each level
        """
        super().__init__()
        self.features = features
        
        # Encoder (downsampling path)
        self.encoder = nn.ModuleList()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Initial encoder block
        self.encoder.append(DoubleConv(in_channels, features[0]))
        
        # Remaining encoder blocks
        for i in range(len(features) - 1):
            self.encoder.append(DoubleConv(features[i], features[i + 1]))
        
        # Decoder (upsampling path)
        self.decoder = nn.ModuleList()
        
        # Reverse features for decoder
        for i in range(len(features) - 1, 0, -1):
            self.decoder.append(
                nn.ConvTranspose2d(features[i], features[i - 1], kernel_size=2, stride=2)
            )
            self.decoder.append(DoubleConv(features[i], features[i - 1]))
        
        # Final output layer
        self.final_conv = nn.Conv2d(features[0], out_channels, kernel_size=1)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through U-Net
        
        Args:
            x: Input tensor of shape (batch, channels, height, width)
            
        Returns:
            Segmentation mask of shape (batch, out_channels, height, width)
        """
        # Encoder path with skip connections
        skip_connections = []
        
        for encoder_block in self.encoder:
            x = encoder_block(x)
            skip_connections.append(x)
            x = self.pool(x)
        
        # Remove last skip connection (before pooling)
        skip_connections = skip_connections[:-1]
        skip_connections = skip_connections[::-1]  # Reverse for decoder
        
        # Decoder path
        for i in range(0, len(self.decoder), 2):
            x = self.decoder[i](x)  # Upsample
            skip_connection = skip_connections[i // 2]
            
            # Handle size mismatch (due to pooling)
            if x.shape != skip_connection.shape:
                x = F.interpolate(x, size=skip_connection.shape[2:], mode='bilinear', align_corners=False)
            
            # Concatenate skip connection
            x = torch.cat([skip_connection, x], dim=1)
            x = self.decoder[i + 1](x)  # Double conv
        
        # Final output
        x = self.final_conv(x)
        return x
    
    def predict(self, x: torch.Tensor) -> torch.Tensor:
        """
        Prediction method for consistency with BaseModel interface
        
        Args:
            x: Input tensor
            
        Returns:
            Segmentation mask
        """
        return self.forward(x)
    
    def predict_mask(self, x: torch.Tensor, threshold: float = 0.5) -> torch.Tensor:
        """
        Predict binary mask with thresholding
        
        Args:
            x: Input tensor
            threshold: Threshold for binary classification
            
        Returns:
            Binary mask
        """
        with torch.no_grad():
            logits = self.forward(x)
            if self.final_conv.out_channels == 1:
                probs = torch.sigmoid(logits)
                return (probs > threshold).float()
            else:
                return torch.argmax(logits, dim=1, keepdim=True).float()


class UNetSmall(UNet):
    """Smaller U-Net variant for faster inference"""
    
    def __init__(self, in_channels: int = 3, out_channels: int = 1):
        super().__init__(in_channels, out_channels, features=[32, 64, 128, 256])


class UNetLarge(UNet):
    """Larger U-Net variant for higher accuracy"""
    
    def __init__(self, in_channels: int = 3, out_channels: int = 1):
        super().__init__(in_channels, out_channels, features=[64, 128, 256, 512, 1024])

