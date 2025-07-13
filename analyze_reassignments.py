#!/usr/bin/env python3
"""
Analysis script for process reassignment tracking data.
Analyzes which processes get reassigned, their sizes, and movement patterns.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
import sys

def analyze_process_reassignments(csv_file):
    print(f"Loading process reassignment data from {csv_file}...")
    df = pd.read_csv(csv_file)
    
    print(f"\n=== BASIC STATISTICS ===")
    print(f"Total reassignments: {len(df):,}")
    print(f"Unique processes moved: {df['ProcessID'].nunique():,}")
    print(f"Unique services: {df['Service'].nunique():,}")
    print(f"Time span: {(df['Timestamp'].max() - df['Timestamp'].min()) / 1000:.2f} seconds")
    
    # Calculate process sizes (sum of requirements)
    print("\nCalculating process sizes...")
    def parse_requirements(req_str):
        try:
            return ast.literal_eval(req_str)
        except:
            return [0, 0, 0, 0]
    
    df['Requirements_List'] = df['Requirements'].apply(parse_requirements)
    df['ProcessSize'] = df['Requirements_List'].apply(sum)
    
    print(f"\n=== PROCESS SIZE ANALYSIS ===")
    print(f"Average process size: {df['ProcessSize'].mean():.0f}")
    print(f"Median process size: {df['ProcessSize'].median():.0f}")
    print(f"Min process size: {df['ProcessSize'].min():.0f}")
    print(f"Max process size: {df['ProcessSize'].max():.0f}")
    
    # Analyze moves per process
    moves_per_process = df['ProcessID'].value_counts()
    print(f"\n=== MOVEMENT FREQUENCY ===")
    print(f"Processes moved once: {(moves_per_process == 1).sum():,}")
    print(f"Processes moved multiple times: {(moves_per_process > 1).sum():,}")
    print(f"Most moved process: Process {moves_per_process.index[0]} with {moves_per_process.iloc[0]} moves")
    
    # Analyze by process size quartiles
    size_quartiles = df['ProcessSize'].quantile([0.25, 0.5, 0.75])
    print(f"\n=== MOVEMENT BY PROCESS SIZE ===")
    print(f"25th percentile size: {size_quartiles[0.25]:.0f}")
    print(f"50th percentile size: {size_quartiles[0.5]:.0f}")
    print(f"75th percentile size: {size_quartiles[0.75]:.0f}")
    
    # Categorize processes by size
    df['SizeCategory'] = pd.cut(df['ProcessSize'], 
                                bins=[0, size_quartiles[0.25], size_quartiles[0.5], size_quartiles[0.75], float('inf')],
                                labels=['Small', 'Medium', 'Large', 'XLarge'])
    
    size_movement_count = df.groupby('SizeCategory').size()
    print("\nMovements by size category:")
    for category, count in size_movement_count.items():
        print(f"  {category}: {count:,} moves ({count/len(df)*100:.1f}%)")
    
    # Analyze improvement over time
    print(f"\n=== IMPROVEMENT ANALYSIS ===")
    print(f"Initial improvement: {df['Improvement'].iloc[0]:.4f}%")
    print(f"Final improvement: {df['Improvement'].iloc[-1]:.4f}%")
    print(f"Total improvement gain: {df['Improvement'].iloc[-1] - df['Improvement'].iloc[0]:.4f}%")
    
    # Analyze move cost distribution
    print(f"\n=== MOVE COST ANALYSIS ===")
    print(f"Average move cost: {df['MoveCost'].mean():.2f}")
    print(f"Median move cost: {df['MoveCost'].median():.2f}")
    print(f"Move cost distribution:")
    move_cost_counts = df['MoveCost'].value_counts().sort_index()
    for cost, count in move_cost_counts.head(10).items():
        print(f"  Cost {cost}: {count:,} moves ({count/len(df)*100:.1f}%)")
    
    # Analyze temporal patterns
    print(f"\n=== TEMPORAL PATTERNS ===")
    df['TimeFromStart'] = (df['Timestamp'] - df['Timestamp'].min()) / 1000  # Convert to seconds
    
    # Divide into time periods
    time_periods = pd.cut(df['TimeFromStart'], bins=5, labels=['Period1', 'Period2', 'Period3', 'Period4', 'Period5'])
    period_stats = df.groupby(time_periods).agg({
        'ProcessSize': 'mean',
        'MoveCost': 'mean',
        'ProcessID': 'count'
    })
    
    print("\nAverage process size moved per time period:")
    for period, stats in period_stats.iterrows():
        print(f"  {period}: {stats['ProcessSize']:.0f} (avg size), {stats['ProcessID']:,} moves")
    
    return df

if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "process_reassignments.csv"
    df = analyze_process_reassignments(csv_file)
    print(f"\nAnalysis complete! Data saved in DataFrame with {len(df)} rows.")
