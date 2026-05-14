#!/usr/bin/env bash
# ============================================================
# DQ Scoring Engine — Quick Setup
# Chạy 1 lần duy nhất khi clone repo về.
# ============================================================
set -e

echo "🚀 DQ Scoring Engine — Setup"
echo "=============================="

# 1. Tạo venv & cài dependencies
if [ ! -d ".venv" ]; then
    echo "📦 Tạo virtual environment..."
    python3 -m venv .venv
fi

echo "📦 Cài dependencies..."
.venv/bin/pip install -q -r requirements.txt

# 2. Kiểm tra data directory
DATA_DIR=""

# Ưu tiên 1: Prep_data nằm cạnh (sibling)
if [ -d "../Prep_data/dq_raw_probe/data" ]; then
    DATA_DIR="../Prep_data/dq_raw_probe/data"
    echo "✅ Tìm thấy Prep_data (sibling): $DATA_DIR"

# Ưu tiên 2: Đang nằm trong Prep_data
elif [ -d "../dq_raw_probe/data" ]; then
    DATA_DIR="../dq_raw_probe/data"
    echo "✅ Tìm thấy Prep_data (parent): $DATA_DIR"

# Không tìm thấy → hỏi user
else
    echo ""
    echo "⚠️  Không tìm thấy thư mục data từ Prep_data."
    echo ""
    echo "Bạn có 2 lựa chọn:"
    echo "  [1] Clone Prep_data về cạnh repo này (recommended)"
    echo "  [2] Chỉ chạy tests với fixtures có sẵn (nhanh)"
    echo ""
    read -p "Chọn (1/2): " choice

    if [ "$choice" = "1" ]; then
        echo "📥 Clone Prep_data..."
        git clone https://github.com/DrMutHo/Prep_data.git ../Prep_data 2>/dev/null || {
            echo "❌ Clone thất bại. Hãy clone thủ công:"
            echo "   git clone https://github.com/DrMutHo/Prep_data.git ../Prep_data"
            echo ""
            echo "Sau đó chạy lại: bash setup.sh"
            exit 1
        }
        DATA_DIR="../Prep_data/dq_raw_probe/data"
        echo "✅ Clone thành công: $DATA_DIR"
    else
        echo "✅ Sẽ chỉ chạy tests với fixtures có sẵn."
    fi
fi

# 3. Chạy tests
echo ""
echo "🧪 Chạy unit tests..."
.venv/bin/python -m unittest tests.test_rules -v 2>&1 | tail -5

# 4. Chạy demo (nếu có data)
if [ -n "$DATA_DIR" ] && [ -d "$DATA_DIR" ]; then
    echo ""
    echo "📊 Chạy scoring demo..."
    .venv/bin/python run_scoring_demo.py --data-dir "$DATA_DIR"
else
    echo ""
    echo "📊 Bỏ qua demo (không có data). Chạy thủ công sau:"
    echo "   .venv/bin/python run_scoring_demo.py --data-dir /đường/dẫn/tới/data"
fi

echo ""
echo "=============================="
echo "✅ Setup hoàn tất!"
echo ""
echo "📌 Cách sử dụng hàng ngày:"
echo "   .venv/bin/python run_scoring_demo.py                    # auto-discover data"
echo "   .venv/bin/python run_scoring_demo.py --data-dir <path>  # chỉ định data"
echo "   .venv/bin/python -m unittest tests.test_rules -v        # chạy tests"
