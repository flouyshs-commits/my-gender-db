import json
from names_dataset import NameDataset

print("正在加载全球 4.9 亿大数据库（首次加载需1-2分钟）...")
nd = NameDataset()

female_only_db = {}
all_names = nd.first_names.keys()

print("正在提炼美国 30-55 岁特征的女性名字...")
for name in all_names:
    name_str = str(name).lower()
    if len(name_str) < 2 or not name_str.isalpha():
        continue

    # 💡 核心修正：新版官方库使用 .search() 替代了旧的 search_first_name
    info = nd.search(name_str)
    if not info or "first_name" not in info:
        continue
    
    fn_info = info["first_name"]
    if not fn_info or "country" not in fn_info or "gender" not in fn_info:
        continue

    # 确保在美国有分布
    countries = fn_info["country"]
    if "United States" not in countries or countries["United States"] < 0.05:
        continue

    # 女性概率大于 65% 的判定为女性
    genders = fn_info["gender"]
    if genders.get("Female", 0.0) >= 0.65:
        female_only_db[name_str] = "F"

# 生成直接可供书签注入的 JS 文件
output_file = "us_female_3055_tps.js"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("window._tpsDb = " + json.dumps(female_only_db, separators=(",", ":")) + ";")

print(f"\n🎉 成功！已生成适合书签注入的文件：{output_file}")
