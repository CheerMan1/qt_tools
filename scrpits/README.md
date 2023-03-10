

#### 1 base64 -> QPixmap
```python
def get_pixmap(data_base64, fmt='png'):
    data = QByteArray().fromBase64(data_base64.encode())
    image = QImage()
    image.loadFromData(data, fmt)
    pix = QPixmap.fromImage(image)
    return pix
```

#### 2 img_file -> base64
```python
def to_base64(file_path, fmt="png"):
    image = QImage(file_path)
    data = QByteArray()
    buffer = QBuffer(data)
    image.save(buffer, fmt)
    return str(data.toBase64())[2:-1]
```