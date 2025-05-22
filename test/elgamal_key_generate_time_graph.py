
import matplotlib.pyplot as plt

# 提取数据
key_sizes = [512, 576, 640, 704, 768, 832, 896, 960, 1024]
avg_times = [16.147893, 47.403437, 48.663082, 48.893848, 26.214356, 33.141076, 72.974650, 106.436910, 290.462504]

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 创建图表
plt.figure(figsize=(12, 6))
plt.plot(key_sizes, avg_times, marker='o', linestyle='-', color='#1f77b4', linewidth=2)

# 添加标题和轴标签（使用英文）
plt.title('Relationship between Key Size and Average Key Generation Time', fontsize=16, pad=20)
plt.xlabel('Key Size (bits)', fontsize=12)
plt.ylabel('Average Key Generation Time (s)', fontsize=12)

# 设置x轴刻度
plt.xticks(key_sizes, rotation=45)

# 添加网格线
plt.grid(True, linestyle='--', alpha=0.7)

# 添加数据标签
for x, y in zip(key_sizes, avg_times):
    plt.annotate(f'{y:.2f}s', (x, y), textcoords='offset points',
                 xytext=(0,5), ha='center', fontsize=9)

# 优化布局
plt.tight_layout()

# 显示图表
plt.show()    





# import time
# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from src.ElGamal.ElGamal import ElGamalKeyGenerator, ElGamal

# def test_key_generation(key_size):
#     times = []
#     for _ in range(3):
#         start = time.perf_counter()
#         alice_public, alice_private = ElGamal.create_keypair(key_size)
#         times.append(time.perf_counter() - start)
    
#     avg_time = sum(times) / 3
#     print(f"Key Size: {key_size} bits, Avg KeyGen Time: {avg_time:.6f}s")
#     return (key_size, avg_time)


# if __name__ == "__main__":
#     results = []
#     for i in range(8):
#         key_size = 512 + i * 128
#         results.append(test_key_generation(key_size))
    
#     # Print summary
#     print("\nSummary Results:")
#     print("KeySize\tAvgKeyGenTime")
#     for size, time in results:
#         print(f"{size}\t{time:.6f}")
