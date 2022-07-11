### demo example:

```python
solution = Solution()
centers = [[100.2, 120.4], [200.1, 210], [210.3, 115.8], [102.5, 200.1]]
result = solution.Hugmatch(centers) # outputs: [[2, 1], [1, 2], [2, 2], [1, 1]]
```

**输入参数**:

- `centers`：所有图片中心的二维坐标组成的列表  [[float, float], [float, float], ...]

**输出参数**：

- `result`: 每一个图片中心坐标对应的正确行、列位置  [[int, int], [int, int], ...]

