# Data Model

## Project
E-Commerce Intelligence & Analytics Platform

## Purpose

The data model defines the main entities required for
e-commerce analytics and their relationships.

## Core Tables

1. customers
2. products
3. categories
4. orders
5. order_items
6. payments
7. returns
8. inventory
9. marketing_campaigns
10. date_dimension

## Table Relationships

customers
    ↓
orders
    ↓
order_items
    ↓
products
    ↓
categories

orders
    ↓
payments

orders / order_items
    ↓
returns

products
    ↓
inventory

marketing_campaigns
    ↓
sales/marketing analysis

date_dimension
    ↓
time-based analysis

## Primary Keys

customers → customer_id
products → product_id
categories → category_id
orders → order_id
order_items → order_item_id
payments → payment_id
returns → return_id
inventory → inventory_id
marketing_campaigns → campaign_id
date_dimension → date

## Main Foreign Keys

orders.customer_id → customers.customer_id

order_items.order_id → orders.order_id

order_items.product_id → products.product_id

products.category_id → categories.category_id

payments.order_id → orders.order_id

returns.order_id → orders.order_id

returns.order_item_id → order_items.order_item_id

inventory.product_id → products.product_id

marketing_campaigns.date → date_dimension.date