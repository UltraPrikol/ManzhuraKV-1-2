"""
ETL Pipeline для анализа продаж интернет-магазина
Этапы: Extract → Transform → Load → Visualize
"""

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sqlalchemy import create_engine, text
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SalesETLPipeline:
    """ETL пайплайн для обработки данных о продажах"""
    
    def __init__(self, csv_path, db_path='sales.db'):
        self.csv_path = csv_path
        self.db_path = db_path
        self.raw_data = None
        self.cleaned_data = None
        self.aggregated_data = None
        
    def extract(self):
        """Этап 1: Извлечение данных из CSV-файла"""
        logger.info("Начало этапа EXTRACT")
        
        try:
            self.raw_data = pd.read_csv(self.csv_path)
            if self.raw_data.empty:
                logger.error(f"Файл {self.csv_path} пуст.")
                raise ValueError("Файл не содержит данных.")
                
            logger.info(f"Загружено {len(self.raw_data)} строк, {len(self.raw_data.columns)} колонок")
            logger.info(f"Колонки: {', '.join(self.raw_data.columns)}")
        except FileNotFoundError:
            logger.error(f"Файл {self.csv_path} не найден")
            raise
        except Exception as e:
            logger.error(f"Ошибка при чтении файла: {e}")
            raise
        
        return self.raw_data
    
    def transform(self):
        """Этап 2: Трансформация и очистка данных"""
        logger.info("Начало этапа TRANSFORM")
        
        if self.raw_data is None:
            logger.error("Нет данных для трансформации. Сначала запустите extract().")
            return None
            
        df = self.raw_data.copy()
        
        # TODO 1: Удалить дубликаты (по всем колонкам)
        initial_count = len(df)
        df = df.drop_duplicates()
        logger.info(f"Удалено дубликатов: {initial_count - len(df)}")
        
        # TODO 4: Преобразование типов данных (выполняем до очистки для корректной фильтрации)
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['price_per_unit'] = pd.to_numeric(df['price_per_unit'], errors='coerce')
        
        # TODO 2: Обработать пропуски (NaN) в разных колонкак
        # - Для числовых колонок: заменить на медиану
        for col in ['quantity', 'price_per_unit']:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            
        # - Для текстовых: заменить на "Unknown"
        text_cols = ['product_name', 'category', 'customer_name', 'customer_city', 'payment_method']
        for col in text_cols:
            df[col] = df[col].fillna("Unknown")
        
        # TODO 3: Фильтрация аномалий (количество <= 0, цена <= 0)
        before_anomaly = len(df)
        df = df[(df['quantity'] > 0) & (df['price_per_unit'] > 0)]
        logger.info(f"Удалено строк с аномальными значениями: {before_anomaly - len(df)}")
        
        # TODO 5: Создать новую колонку total_amount = quantity * price_per_unit
        df['total_amount'] = df['quantity'] * df['price_per_unit']
        
        # TODO 6: Обогащение данных (добавить колонку month_year из order_date)
        # Удаляем строки, где дата не смогла распознаться
        df = df.dropna(subset=['order_date'])
        df['month_year'] = df['order_date'].dt.strftime('%Y-%m')
        
        self.cleaned_data = df
        logger.info(f"После очистки: {len(df)} строк")
        
        return self.cleaned_data
    
    def aggregate(self):
        """Этап 3: Агрегация данных для аналитики"""
        logger.info("Начало этапа AGGREGATE")
        
        if self.cleaned_data is None:
            logger.error("Нет данных для агрегации.")
            return None
            
        df = self.cleaned_data.copy()
        
        # Группировка по category и month_year
        self.aggregated_data = df.groupby(['category', 'month_year']).agg({
            'quantity': 'sum',
            'total_amount': 'sum',
            'price_per_unit': 'mean',
            'order_id': 'nunique'
        }).rename(columns={
            'quantity': 'total_quantity',
            'total_amount': 'total_revenue',
            'price_per_unit': 'avg_price',
            'order_id': 'order_count'
        }).reset_index()
        
        logger.info(f"Агрегация завершена. Сформировано {len(self.aggregated_data)} аналитических строк.")
        return self.aggregated_data
    
    def load_to_sqlite(self):
        """Этап 4: Загрузка данных в SQLite базу данных"""
        logger.info("Начало этапа LOAD")
        
        if self.cleaned_data is None or self.aggregated_data is None:
            logger.error("Данные для загрузки отсутствуют.")
            return
            
        # Создание подключения
        engine = create_engine(f'sqlite:///{self.db_path}')
        
        # TODO 1-3: Сохранить таблицы и заменить, если существуют
        self.cleaned_data.to_sql('sales_cleaned', engine, if_exists='replace', index=False)
        self.aggregated_data.to_sql('sales_aggregated', engine, if_exists='replace', index=False)
        
        # Проверка: вывести список таблиц в базе
        with engine.connect() as conn:
            tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
            logger.info(f"Таблицы в БД: {[t[0] for t in tables]}")
            
        logger.info(f"Данные успешно загружены в {self.db_path}")
        
    def visualize(self):
        """Этап 5: Визуализация результатов (3 графика)"""
        logger.info("Начало этапа VISUALIZE")
        
        if self.aggregated_data is None:
            logger.error("Нет данных для визуализации.")
            return
            
        sns.set_style("whitegrid")
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # График 1: Выручка по категориям (barplot)
        category_revenue = self.aggregated_data.groupby('category')['total_revenue'].sum().sort_values(ascending=False).reset_index()
        sns.barplot(data=category_revenue, x='category', y='total_revenue', ax=axes[0], palette='viridis')
        axes[0].set_title('Выручка по категориям товаров', fontsize=12)
        axes[0].set_xlabel('Категория')
        axes[0].set_ylabel('Выручка (руб.)')
        axes[0].tick_params(axis='x', rotation=30)
        
        # График 2: Динамика продаж по месяцам (lineplot)
        sns.lineplot(data=self.aggregated_data, x='month_year', y='total_revenue', hue='category', marker='o', ax=axes[1])
        axes[1].set_title('Динамика продаж по месяцам', fontsize=12)
        axes[1].set_xlabel('Месяц')
        axes[1].set_ylabel('Выручка (руб.)')
        
        # График 3: Доля категорий в общей выручке (pie chart)
        pie_data = self.aggregated_data.groupby('category')['total_revenue'].sum()
        axes[2].pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        axes[2].set_title('Доля категорий в общей выручке', fontsize=12)
        
        plt.tight_layout()
        plt.savefig('report/graphs/sales_analytics.png') # сохранение графиков в отчет
        plt.show()
        
    def run(self):
        """Запуск полного ETL-пайплайна"""
        logger.info("=" * 50)
        logger.info("ЗАПУСК ETL ПАЙПЛАЙНА")
        logger.info("=" * 50)
        
        self.extract()
        self.transform()
        self.aggregate()
        self.load_to_sqlite()
        self.visualize()
        
        logger.info("ETL пайплайн успешно завершён")


if __name__ == "__main__":
    # Перед запуском убедись, что папки report/graphs/ и data/ существуют!
    import os
    os.makedirs('data', exist_ok=True)
    os.makedirs('report/graphs', exist_ok=True)
    
    pipeline = SalesETLPipeline('data/sales.csv', 'sales.db')
    pipeline.run()