import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="محل العطور - نظام الإدارة",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #8B4513;
        font-size: 2.5em;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Database initialization
def init_db():
    conn = sqlite3.connect('perfume_shop.db')
    c = conn.cursor()
    
    c.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        price_100g REAL,
        price_500g REAL,
        price_1kg REAL,
        price_5kg REAL,
        stock_100g INTEGER,
        stock_500g INTEGER,
        stock_1kg INTEGER,
        stock_5kg INTEGER
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        address TEXT,
        date_created TEXT
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        address TEXT,
        date_created TEXT
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        customer_name TEXT,
        product_name TEXT,
        size TEXT,
        quantity INTEGER,
        unit_price REAL,
        total_price REAL,
        date_sale TEXT
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY,
        supplier_name TEXT,
        product_name TEXT,
        size TEXT,
        quantity INTEGER,
        unit_price REAL,
        total_price REAL,
        date_purchase TEXT
    )""")
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Sidebar menu
st.sidebar.title("🏪 محل العطور")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "القائمة الرئيسية",
    ["🏠 الرئيسية", "📦 المنتجات", "👥 العملاء", "🚚 الموردين", "🛒 فواتير البيع", "📥 فواتير الشراء", "📊 التقارير"]
)

st.sidebar.markdown("---")
st.sidebar.info("نظام إدارة متجر العطور\nمتطور بواسطة Streamlit")

# ============ HOME PAGE ============
if page == "🏠 الرئيسية":
    st.markdown("<h1 class='main-title'>🏪 مرحباً بك في نظام إدارة محل العطور</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    conn = sqlite3.connect('perfume_shop.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM products")
    num_products = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM customers")
    num_customers = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM suppliers")
    num_suppliers = c.fetchone()[0]
    
    c.execute("SELECT SUM(total_price) FROM sales WHERE date_sale >= date('now', '-30 days')")
    total_sales_month = c.fetchone()[0] or 0
    
    c.execute("SELECT SUM(total_price) FROM sales")
    total_sales = c.fetchone()[0] or 0
    
    conn.close()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 عدد المنتجات", f"{num_products}", delta=None)
    with col2:
        st.metric("👥 عدد العملاء", f"{num_customers}", delta=None)
    with col3:
        st.metric("🚚 عدد الموردين", f"{num_suppliers}", delta=None)
    with col4:
        st.metric("💰 إجمالي المبيعات", f"{total_sales:,.0f} دج", delta=None)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"🔥 المبيعات خلال آخر 30 يوم: {total_sales_
