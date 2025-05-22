import matplotlib.pyplot as plt

# 数据
key_sizes = [2048, 2176, 2304, 2432, 2560, 2688, 2816, 2944, 3072, 3200, 3328, 3456, 3584, 3712, 3840, 3968]
avg_times = [2.571675, 2.266838, 3.378178, 3.767596, 4.306194, 6.156540, 7.195320, 7.766657, 
             8.927467, 8.663682, 11.637862, 13.451822, 9.619351, 10.608393, 22.726179,37.514026]

# 创建图表
plt.figure(figsize=(12, 6))  # 设置画布大小
plt.plot(key_sizes, avg_times, marker='o', linestyle='-', color='#1f77b4', linewidth=2)  # 绘制折线图

# 添加标题和轴标签
plt.title('Relationship between Key Size and Average Key Generation Time', fontsize=16, pad=20)
plt.xlabel('Key Size (KeySize)', fontsize=12)
plt.ylabel('Average Key Generation Time (Seconds)', fontsize=12)
# 自定义x轴刻度（每256间隔显示刻度）
plt.xticks(range(2048, 4097, 256), rotation=45, ha='right')  # 旋转刻度标签避免重叠

# 添加网格线
plt.grid(True, linestyle='--', alpha=0.7)

# 显示数值标签（可选）
for x, y in zip(key_sizes, avg_times):
    plt.text(x, y, f'{y:.2f}', ha='right', va='bottom', fontsize=10)

# 优化布局
plt.tight_layout()
plt.show()








# import time
# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from src.RSA.rsa import RSAKeyGenerator

# def test_key_generation(key_size):
#     times = []
#     for _ in range(3):
#         start = time.perf_counter()
#         private_key, public_key = RSAKeyGenerator.generate_keypair(key_size)
#         times.append(time.perf_counter() - start)
    
#     avg_time = sum(times) / 3
#     print(f"Key Size: {key_size} bits, Avg KeyGen Time: {avg_time:.6f}s")
#     return (key_size, avg_time)

# if __name__ == "__main__":
#     results = []
#     # Test from 2048 to 2048+128*15 in steps of 128
#     for i in range(16):
#         key_size = 2048 + i * 128
#         results.append(test_key_generation(key_size))
    
#     # Print summary
#     print("\nSummary Results:")
#     print("KeySize\tAvgKeyGenTime")
#     for size, time in results:
#         print(f"{size}\t{time:.6f}")

