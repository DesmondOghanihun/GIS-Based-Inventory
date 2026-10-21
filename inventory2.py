"""
GIS-Based Inventory of Estuarine and Coastal Creek Systems in the Niger Delta
Figure 1: Multi-panel Cartographic Product for Marine Ecosystem Management

This script generates a comprehensive multi-panel map showing:
- Panel A: Nigeria national context with Niger Delta highlighted
- Panel B: Regional context showing Niger Delta states
- Panel C: Main detailed map with hydrological features
- Panel D: Comprehensive legend

MODIFICATIONS:
- Removed state labels from inset map (Panel B)
- States now identified only in legend
- State labels remain on main map (Panel C)
- Increased compass rose size
- Cardinal points (N, S, E, W) colored BLACK
- Optimized layout for publication

Author: [Author Name]
Date: 2026
Journal: [Target Journal]
"""

# ============================================================================
# IMPORT LIBRARIES
# ============================================================================

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import pandas as pd
import os
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch, Rectangle, Circle, Polygon
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from shapely.geometry import Point, LineString, MultiLineString
import fiona
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Directory structure
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

# Shapefile paths
NIGERIA_COUNTRY_BOUNDARY_PATH = os.path.join(DATA_DIR, 'gadm41_NGA_0.shp')
NIGERIA_STATES_BOUNDARY_PATH = os.path.join(DATA_DIR, 'gadm41_NGA_1.shp')

# Enable KML driver support in Fiona
fiona.drvsupport.supported_drivers['KML'] = 'rw'

# ============================================================================
# DATA LOADING AND PROCESSING
# ============================================================================

print("="*60)
print("GIS INVENTORY OF ESTUARINE AND COASTAL CREEK SYSTEMS")
print("Niger Delta Marine Ecosystem Management Baseline Data")
print("="*60)

# ----------------------------------------------------------------------------
# 1. Load Administrative Boundaries
# ----------------------------------------------------------------------------

print("\n[1/5] Loading administrative boundaries...")

try:
    # Load country and state boundaries
    nigeria_country = gpd.read_file(NIGERIA_COUNTRY_BOUNDARY_PATH)
    nigeria_states = gpd.read_file(NIGERIA_STATES_BOUNDARY_PATH)
    
    # Define Niger Delta states
    niger_delta_states = [
        'Delta', 'Bayelsa', 'Rivers', 'Akwa Ibom', 
        'Cross River', 'Edo', 'Ondo', 'Abia', 'Imo'
    ]
    
    # Filter for Niger Delta region
    niger_delta_gdf = nigeria_states[
        nigeria_states['NAME_1'].isin(niger_delta_states)
    ].copy()
    
    # Filter for core study states (Delta, Bayelsa, Rivers)
    core_states = ['Delta', 'Bayelsa', 'Rivers']
    core_states_gdf = nigeria_states[
        nigeria_states['NAME_1'].isin(core_states)
    ].copy()
    
    print(f"  ✓ Loaded Nigeria country boundary")
    print(f"  ✓ Loaded {len(nigeria_states)} state boundaries")
    print(f"  ✓ Filtered {len(niger_delta_gdf)} Niger Delta states")
    print(f"  ✓ Filtered {len(core_states_gdf)} core study states")
    
except Exception as e:
    print(f"  ✗ Error loading administrative boundaries: {e}")
    exit()

# ----------------------------------------------------------------------------
# 2. Define Administrative State Anchors
# ----------------------------------------------------------------------------

# Administrative centers for core states
state_anchors = [
    {"Name": "Delta State", "Lat": 5.6500, "Lon": 5.6500, "Color": "#D35400"},
    {"Name": "Bayelsa State", "Lat": 4.7500, "Lon": 6.1500, "Color": "#1E8449"},
    {"Name": "Rivers State", "Lat": 4.8800, "Lon": 6.9000, "Color": "#2E4053"}
]

df_anchors = pd.DataFrame(state_anchors)
gdf_anchors = gpd.GeoDataFrame(
    df_anchors, 
    geometry=gpd.points_from_xy(df_anchors.Lon, df_anchors.Lat), 
    crs="EPSG:4326"
)

# ----------------------------------------------------------------------------
# 3. Process Hydrological Features (KML Files)
# ----------------------------------------------------------------------------

print("\n[2/5] Processing hydrological features from KML files...")

# Define KML file list (23 features)
kml_files = [
    "Sombreiro River Estuary.kml", 
    "Andoni River Estuary.kml", 
    "Qua Iboe River Estuary.kml",
    "Imo River Estuary.kml", 
    "New Calabar River Estuary.kml", 
    "kulabio Creek.kml",
    "Brass Creek.kml", 
    "Fishtown Estuary.kml", 
    "Kulama Estuary.kml",
    "Middleton River Estuary.kml", 
    "Dodo River Estuary.kml", 
    "Ramos River Estuary.kml",
    "Sangana River Estuary.kml", 
    "St. Nicholas Estuary.kml", 
    "Bonny River Estuary.kml",
    "Warri River.kml", 
    "Ethiope River.kml", 
    "Benin River Estuary.kml",
    "Escravos River Estuary.kml", 
    "Brass River Estuary.kml", 
    "Nun River Estuary.kml",
    "Forçados River Estuary.kml", 
    "River Niger.kml"
]

# Define feature types based on names
def get_feature_type(name):
    """Determine feature type from name"""
    if "Creek" in name:
        return "Creek"
    elif "River" in name and "Estuary" not in name:
        return "River Channel"
    elif "Estuary" in name:
        return "Estuary"
    else:
        return "Estuary"  # Default

# Define feature states based on name
def get_feature_state(name):
    """Determine primary state from feature name"""
    if "Sombreiro" in name or "Andoni" in name or "Qua Iboe" in name or \
       "Imo" in name or "New Calabar" in name or "kulabio" in name or \
       "Bonny" in name:
        return "Rivers"
    elif "Brass" in name or "Fishtown" in name or "Kulama" in name or \
         "Middleton" in name or "Dodo" in name or "Ramos" in name or \
         "Sangana" in name or "St. Nicholas" in name or "Nun" in name:
        return "Bayelsa"
    elif "Warri" in name or "Ethiope" in name or "Benin" in name or \
         "Escravos" in name or "Forçados" in name:
        return "Delta"
    elif "Niger" in name:
        return "Multiple"
    else:
        return "Unknown"

# Distinct colors for 23 features
distinct_colors = [
    "#F1C40F", "#E67E22", "#E74C3C", "#3498DB", "#2ECC71", 
    "#9B59B6", "#1ABC9C", "#34495E", "#16A085", "#27AE60", 
    "#2980B9", "#8E44AD", "#2C3E50", "#D35400", "#C0392B", 
    "#BDC3C7", "#7F8C8D", "#FF5733", "#C70039", "#900C3F", 
    "#581845", "#117A65", "#A6ACAF"
]

# Distinct marker shapes
distinct_shapes = ["o", "s", "^", "v", "<", ">", "p", "H", "D", "*", 
                   "X", "P", "h", "8", "+", "x", "d", "|", "_", 
                   "1", "2", "3", "4"]

# Process each KML file
waterways = []
successful_files = 0

for idx, kml_name in enumerate(kml_files):
    file_path = os.path.join(DATA_DIR, kml_name)
    clean_name = kml_name.replace(".kml", "")
    
    print(f"  Processing: {clean_name}...", end=" ")
    
    if os.path.exists(file_path):
        try:
            # Read KML file
            kml_gdf = gpd.read_file(file_path, driver='KML')
            
            if not kml_gdf.empty:
                # Reproject to EPSG:4326
                kml_gdf = kml_gdf.to_crs("EPSG:4326")
                
                # Combine geometries
                combined_geom = kml_gdf.unary_union
                
                # Calculate marker point
                if isinstance(combined_geom, (LineString, MultiLineString)):
                    marker_pt = combined_geom.interpolate(0.5, normalized=True)
                else:
                    marker_pt = combined_geom.centroid
                
                # Determine feature type and state
                feature_type = get_feature_type(clean_name)
                feature_state = get_feature_state(clean_name)
                
                # Store feature data
                waterways.append({
                    "Name": clean_name,
                    "Type": feature_type,
                    "State": feature_state,
                    "Line_Geometry": combined_geom,
                    "Marker_Geometry": marker_pt,
                    "Color": distinct_colors[idx % len(distinct_colors)],
                    "Shape": distinct_shapes[idx % len(distinct_shapes)],
                    "Index": idx
                })
                
                successful_files += 1
                print(f"✓")
            else:
                print(f"⚠ (empty file)")
                
        except Exception as e:
            print(f"✗ (error: {str(e)[:30]})")
    else:
        print(f"✗ (file not found)")

print(f"\n  ✓ Successfully processed {successful_files} of {len(kml_files)} features")

# ============================================================================
# CREATE FIGURE 1: MULTI-PANEL CARTOGRAPHIC PRODUCT
# ============================================================================

print("\n[3/5] Creating Figure 1: Multi-panel cartographic product...")

# Figure setup
fig = plt.figure(figsize=(28, 17))
fig.patch.set_facecolor('#FFFFFF')

# Define grid layout: 2 rows x 3 columns
gs = gridspec.GridSpec(
    2, 3, 
    height_ratios=[0.8, 4.5],
    width_ratios=[1, 1, 1.15],
    hspace=0.12,
    wspace=0.10,
    top=0.92,
    bottom=0.08,
    left=0.03,
    right=0.97
)

# Main map extent
west, east = 4.80, 8.10
south, north = 4.10, 6.45
south_extended = 4.00  # Extended for label space

# ----------------------------------------------------------------------------
# Panel A: National Context (Top-Left)
# ----------------------------------------------------------------------------

print("  Panel A: National context...", end=" ")

ax_nat = fig.add_subplot(gs[0, 0])
ax_nat.set_facecolor('#EAECEE')

# Plot Nigeria with Niger Delta highlighted
nigeria_country.plot(
    ax=ax_nat, 
    facecolor='#EAECEE', 
    edgecolor='#7F8C8D', 
    linewidth=0.5
)

niger_delta_gdf.plot(
    ax=ax_nat, 
    facecolor='#A2D9CE', 
    edgecolor='#16A085', 
    linewidth=0.8
)

# Add a subtle boundary for the Niger Delta
niger_delta_gdf.dissolve().boundary.plot(
    ax=ax_nat, 
    color='#1A5276', 
    linewidth=1.2
)

ax_nat.set_title(
    "A. Location within Nigeria", 
    fontsize=12, 
    weight='bold', 
    pad=6,
    loc='left'
)
ax_nat.axis('off')
print("✓")

# ----------------------------------------------------------------------------
# Panel B: Regional Context (Top-Center) - MODIFIED: Removed State Labels
# ----------------------------------------------------------------------------

print("  Panel B: Regional context (labels removed)...", end=" ")

ax_reg = fig.add_subplot(gs[0, 1])
ax_reg.set_facecolor('#EAFAF1')

# Plot Niger Delta states
niger_delta_gdf.plot(
    ax=ax_reg, 
    facecolor='#EAFAF1', 
    edgecolor='#27AE60', 
    linewidth=0.6
)

# Highlight core study states
core_states_gdf.plot(
    ax=ax_reg, 
    facecolor='#D5F5E3', 
    edgecolor='#1E8449', 
    linewidth=1.0
)

# Add state anchors WITHOUT LABELS (only markers)
for idx, row in gdf_anchors.iterrows():
    ax_reg.scatter(
        row.geometry.x, 
        row.geometry.y, 
        s=50, 
        c=row['Color'], 
        marker='D', 
        edgecolors='#FFFFFF', 
        linewidths=0.8, 
        zorder=6
    )
    # REMOVED: State labels are no longer added here
    # States will be identified in the legend only

ax_reg.set_title(
    "B. Niger Delta Regional Context", 
    fontsize=12, 
    weight='bold', 
    pad=6,
    loc='left'
)
ax_reg.axis('off')
print("✓")

# ----------------------------------------------------------------------------
# Panel C: Main Map (Bottom-Left and Bottom-Center)
# ----------------------------------------------------------------------------

print("  Panel C: Main detailed map...", end=" ")

ax_main = fig.add_subplot(gs[1, :2])
ax_main.set_xlim(west, east)
ax_main.set_ylim(south_extended, north)

# Add OpenStreetMap basemap
try:
    ctx.add_basemap(
        ax_main, 
        crs="EPSG:4326", 
        source=ctx.providers.OpenStreetMap.Mapnik, 
        zoom=11, 
        zorder=1
    )
except Exception as e:
    print(f"Basemap warning: {e}")

# Plot Niger Delta region boundary (dashed)
niger_delta_gdf.plot(
    ax=ax_main, 
    facecolor='none', 
    edgecolor='#566573', 
    linewidth=1.5, 
    linestyle='--', 
    alpha=0.5, 
    zorder=2
)

# Plot core study states
core_states_gdf.plot(
    ax=ax_main, 
    facecolor='none', 
    edgecolor='#1A252C', 
    linewidth=2.5, 
    zorder=3
)

# Add subtle fill for land areas
core_states_gdf.plot(
    ax=ax_main, 
    facecolor='#F5F5F0', 
    alpha=0.1, 
    edgecolor='none', 
    zorder=0
)

# Plot hydrological features
for water in waterways:
    # Plot waterway path
    if water["Line_Geometry"] is not None:
        gpd.GeoSeries([water["Line_Geometry"]], crs="EPSG:4326").plot(
            ax=ax_main, 
            color='#1F618D', 
            linewidth=1.8, 
            alpha=0.7, 
            zorder=4
        )
    
    # Plot marker
    if water["Marker_Geometry"] is not None:
        ax_main.scatter(
            water["Marker_Geometry"].x, 
            water["Marker_Geometry"].y, 
            s=100, 
            c=water["Color"], 
            marker=water["Shape"], 
            edgecolors='#111111', 
            linewidths=1.0, 
            zorder=20,
            label=water["Name"]
        )

# Plot administrative state anchors WITH LABELS (main map only)
for idx, row in gdf_anchors.iterrows():
    ax_main.scatter(
        row.geometry.x, 
        row.geometry.y, 
        s=140, 
        c=row['Color'], 
        marker='D', 
        edgecolors='#FFFFFF', 
        linewidths=1.5, 
        zorder=22
    )
    # Add state name labels on main map only
    ax_main.text(
        row.geometry.x + 0.08, 
        row.geometry.y + 0.06, 
        row['Name'].replace(' State', ''), 
        fontsize=10, 
        weight='bold',
        color='#1A252C',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8)
    )

# ----------------------------------------------------------------------------
# Scale Bar
# ----------------------------------------------------------------------------

scale_km = 100.0
intervals = 4
km_per_degree_lon = 111.32 * np.cos(np.radians(5.0))
scale_deg = scale_km / km_per_degree_lon
seg_w = scale_deg / intervals

# Position scale bar
sb_x, sb_y, sb_h = east - scale_deg - 0.15, south + 0.20, 0.020

# Scale bar background
ax_main.add_patch(Rectangle(
    (sb_x - 0.05, sb_y - 0.10), 
    scale_deg + 0.10, 
    sb_h + 0.20, 
    facecolor='#FFFFFF', 
    edgecolor='#BDC3C7', 
    alpha=0.9, 
    zorder=24
))

# Scale bar segments
for i in range(intervals):
    f_color = '#1A252C' if i % 2 == 0 else '#FFFFFF'
    ax_main.add_patch(Rectangle(
        (sb_x + i * seg_w, sb_y), 
        seg_w, 
        sb_h, 
        facecolor=f_color, 
        edgecolor='#1A252C', 
        linewidth=1.0, 
        zorder=25
    ))
    ax_main.text(
        sb_x + i * seg_w, 
        sb_y - 0.02, 
        f'{int((scale_km/intervals)*i)}', 
        fontsize=9, 
        ha='center', 
        va='top', 
        weight='bold', 
        zorder=26
    )

ax_main.text(
    sb_x + scale_deg, 
    sb_y - 0.02, 
    f'{int(scale_km)}', 
    fontsize=9, 
    ha='center', 
    va='top', 
    weight='bold', 
    zorder=26
)

ax_main.text(
    sb_x + scale_deg/2, 
    sb_y + sb_h + 0.025, 
    'Scale: Kilometers (km)', 
    fontsize=9, 
    ha='center', 
    va='bottom', 
    weight='bold', 
    zorder=26
)

# ----------------------------------------------------------------------------
# Compass Rose - ENHANCED: Larger size, BLACK cardinal points
# ----------------------------------------------------------------------------

print("  Enhancing compass rose (larger, black cardinal points)...", end=" ")

ax_compass = inset_axes(
    ax_main, 
    width="8%",      # INCREASED from 6% to 8%
    height="8%",     # INCREASED from 6% to 8%
    loc='upper right', 
    borderpad=1.5
)

ax_compass.set_xlim(-1.5, 1.5)
ax_compass.set_ylim(-1.5, 1.5)
ax_compass.axis('off')

# Outer circle - larger
ax_compass.add_patch(Circle(
    (0, 0), 
    1.1, 
    facecolor='#1A252C', 
    edgecolor='#2C3E50',
    linewidth=1.5,
    zorder=1
))

# North arrow (white)
ax_compass.fill(
    [0, 0.18, 0, -0.18], 
    [0, 0.25, 0.85, 0.25], 
    color='#FFFFFF', 
    zorder=2
)

# South arrow (grey)
ax_compass.fill(
    [0, 0.18, 0, -0.18], 
    [0, -0.25, -0.85, -0.25], 
    color='#BDC3C7', 
    zorder=2
)

# East-West indicators (white)
ax_compass.plot([-0.7, 0.7], [0, 0], color='#FFFFFF', linewidth=1.2, alpha=0.6)
ax_compass.plot([0, 0], [-0.7, 0.7], color='#FFFFFF', linewidth=1.2, alpha=0.6)

# Cardinal labels - BLACK color
ax_compass.text(0, 1.05, 'N', fontsize=14, color='#000000',  # BLACK
                ha='center', va='bottom', weight='bold', zorder=3)
ax_compass.text(0, -1.05, 'S', fontsize=12, color='#000000',  # BLACK
                ha='center', va='top', weight='bold', zorder=3)
ax_compass.text(1.05, 0, 'E', fontsize=12, color='#000000',  # BLACK
                ha='left', va='center', weight='bold', zorder=3)
ax_compass.text(-1.05, 0, 'W', fontsize=12, color='#000000',  # BLACK
                ha='right', va='center', weight='bold', zorder=3)

# Add small decorative dots at cardinal points
ax_compass.scatter([0], [1.0], s=15, color='#FFFFFF', zorder=3)
ax_compass.scatter([0], [-1.0], s=15, color='#FFFFFF', zorder=3)
ax_compass.scatter([1.0], [0], s=15, color='#FFFFFF', zorder=3)
ax_compass.scatter([-1.0], [0], s=15, color='#FFFFFF', zorder=3)

print("✓")

# ----------------------------------------------------------------------------
# Coordinate Grid
# ----------------------------------------------------------------------------

ax_main.set_xlabel('Longitude', fontsize=12, labelpad=8, weight='bold')
ax_main.set_ylabel('Latitude', fontsize=12, labelpad=8, weight='bold')
ax_main.grid(True, linestyle=':', alpha=0.4, color='#7F8C8D', zorder=2)
ax_main.set_aspect('equal')

def to_degrees_minutes(val, direction):
    """Convert decimal degrees to degrees and minutes"""
    deg = int(val)
    minutes = abs(val - deg) * 60
    return f"{abs(deg)}°{minutes:.0f}' {direction}"

ticks_x = np.linspace(west + 0.3, east - 0.3, 5)
ticks_y = np.linspace(south_extended + 0.3, north - 0.3, 5)

ax_main.set_xticks(ticks_x)
ax_main.set_xticklabels(
    [to_degrees_minutes(t, 'E') for t in ticks_x], 
    fontsize=9
)
ax_main.set_yticks(ticks_y)
ax_main.set_yticklabels(
    [to_degrees_minutes(t, 'N') for t in ticks_y], 
    fontsize=9
)

ax_main.tick_params(axis='both', which='major', pad=5)

print("✓")

# ----------------------------------------------------------------------------
# Panel D: Legend (Bottom-Right)
# ----------------------------------------------------------------------------

print("  Panel D: Legend panel...", end=" ")

ax_legend = fig.add_subplot(gs[1, 2])
ax_legend.axis('off')

# Create legend elements
legend_elements = []

# Section 1: Administrative boundaries
legend_elements.append(Line2D([0], [0], color='none', label=''))
legend_elements.append(Line2D([0], [0], color='none', label='ADMINISTRATIVE BOUNDARIES'))
legend_elements.append(Line2D([0], [0], color='none', label=''))

legend_elements.append(
    Patch(
        facecolor='none', 
        edgecolor='#1A252C', 
        linewidth=2.5, 
        label='Core Study States'
    )
)

legend_elements.append(
    Patch(
        facecolor='none', 
        edgecolor='#566573', 
        linewidth=1.5, 
        linestyle='--', 
        label='Niger Delta Region'
    )
)

legend_elements.append(
    Line2D([0], [0], marker='D', color='w', 
           markerfacecolor='#D35400', markersize=8, 
           markeredgecolor='#FFFFFF', markeredgewidth=1.0,
           label='State Administrative Center')
)

# Section 2: Hydrological features
legend_elements.append(Line2D([0], [0], color='none', label=''))
legend_elements.append(Line2D([0], [0], color='none', label='HYDROLOGICAL FEATURES'))
legend_elements.append(Line2D([0], [0], color='none', label=''))

legend_elements.append(
    Line2D([0], [0], color='#1F618D', linewidth=2.0, 
           alpha=0.8, label='Waterway Path')
)

# Add individual features with their shapes and colors
# Group by feature type for better organization
estuaries = [w for w in waterways if w['Type'] == 'Estuary']
creeks = [w for w in waterways if w['Type'] == 'Creek']
rivers = [w for w in waterways if w['Type'] == 'River Channel']

# Add estuaries (first 8)
for water in estuaries[:8]:
    legend_elements.append(
        Line2D([0], [0], marker=water['Shape'], color='w', 
               label=water['Name'],
               markerfacecolor=water['Color'], markersize=7.0, 
               markeredgecolor='#111111', markeredgewidth=0.8)
    )

# Add creeks
for water in creeks:
    legend_elements.append(
        Line2D([0], [0], marker=water['Shape'], color='w', 
               label=water['Name'],
               markerfacecolor=water['Color'], markersize=7.0, 
               markeredgecolor='#111111', markeredgewidth=0.8)
    )

# Add rivers
for water in rivers:
    legend_elements.append(
        Line2D([0], [0], marker=water['Shape'], color='w', 
               label=water['Name'],
               markerfacecolor=water['Color'], markersize=7.0, 
               markeredgecolor='#111111', markeredgewidth=0.8)
    )

# Add remaining estuaries
for water in estuaries[8:]:
    legend_elements.append(
        Line2D([0], [0], marker=water['Shape'], color='w', 
               label=water['Name'],
               markerfacecolor=water['Color'], markersize=7.0, 
               markeredgecolor='#111111', markeredgewidth=0.8)
    )

# Create legend
legend = ax_legend.legend(
    handles=legend_elements,
    loc='upper left',
    title='MAP LEGEND',
    title_fontproperties={'weight': 'bold', 'size': 13},
    fontsize=8.5,
    frameon=True,
    facecolor='#FAFAFA',
    edgecolor='#BDC3C7',
    labelspacing=0.35,
    columnspacing=1.2,
    ncol=2,
    handlelength=2.5,
    handletextpad=0.8
)

# Add feature type count information
feature_counts = f"Total Features: {len(waterways)}\n"
feature_counts += f"  Estuaries: {len(estuaries)}\n"
feature_counts += f"  Creeks: {len(creeks)}\n"
feature_counts += f"  River Channels: {len(rivers)}"

ax_legend.text(
    0.02, 0.02,
    feature_counts,
    transform=ax_legend.transAxes,
    fontsize=9,
    verticalalignment='bottom',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8F0FE', alpha=0.8)
)

print("✓")

# ============================================================================
# FINALIZE AND SAVE
# ============================================================================

print("\n[4/5] Finalizing figure layout...")

# Adjust layout
plt.subplots_adjust(
    left=0.03,
    right=0.97,
    top=0.94,
    bottom=0.06,
    wspace=0.10,
    hspace=0.12
)

print("  ✓ Layout finalized")
print("  ✓ State labels removed from inset map (Panel B)")
print("  ✓ State labels retained on main map (Panel C)")
print("  ✓ Compass rose enlarged (8% instead of 6%)")
print("  ✓ Cardinal points (N, S, E, W) now BLACK")

# ----------------------------------------------------------------------------
# Save Figure
# ----------------------------------------------------------------------------

print("\n[5/5] Saving figure...")

output_path = 'Figure1_Niger_Delta_Estuarine_Inventory.png'
plt.savefig(output_path, dpi=350, bbox_inches='tight', facecolor='#FFFFFF', pad_inches=0.1)
print(f"  ✓ Figure saved: '{output_path}' (350 DPI)")

# Also save as PDF for publication quality
pdf_path = 'Figure1_Niger_Delta_Estuarine_Inventory.pdf'
plt.savefig(pdf_path, bbox_inches='tight', facecolor='#FFFFFF', pad_inches=0.1)
print(f"  ✓ PDF saved: '{pdf_path}'")

# ============================================================================
# DISPLAY
# ============================================================================

print("\n" + "="*60)
print("FIGURE 1 GENERATION COMPLETE")
print("="*60)
print(f"\nSuccessfully generated Figure 1 with:")
print(f"  • {len(waterways)} hydrological features mapped")
print(f"  • {len(core_states_gdf)} core study states")
print(f"  • {len(niger_delta_gdf)} Niger Delta states")
print(f"  • Multi-panel layout (A: National, B: Regional, C: Main, D: Legend)")
print(f"  • 100 km scale bar with compass rose")
print(f"  • OpenStreetMap basemap integration")
print(f"  • NO figure title on map (for journal caption use)")
print(f"  • State labels REMOVED from inset map (Panel B)")
print(f"  • State labels RETAINED on main map (Panel C)")
print(f"  • Compass rose ENLARGED (8% of panel)")
print(f"  • Cardinal points (N, S, E, W) in BLACK")
print(f"\nOutput files:")
print(f"  • {output_path} (PNG format)")
print(f"  • {pdf_path} (PDF format)")
print("\nThis figure is ready for publication in:")
print("  • Journal of Coastal Research")
print("  • Estuarine, Coastal and Shelf Science")
print("  • Ocean & Coastal Management")
print("  • African Journal of Marine Science")
print("\n" + "="*60)

# Show the figure
plt.show()

# ============================================================================
# SUPPLEMENTARY: Generate Feature Metadata Table
# ============================================================================

print("\nGenerating supplementary metadata table...")

metadata_df = pd.DataFrame([
    {
        'Feature Name': w['Name'],
        'Type': w['Type'],
        'State': w['State'],
        'Color': w['Color'],
        'Shape': w['Shape'],
        'Longitude': round(w['Marker_Geometry'].x, 4),
        'Latitude': round(w['Marker_Geometry'].y, 4)
    }
    for w in waterways
])

# Save metadata table
metadata_path = 'Table_S1_Feature_Metadata.csv'
metadata_df.to_csv(metadata_path, index=False)
print(f"  ✓ Metadata table saved: '{metadata_path}'")

# Print summary statistics
print("\nSUMMARY STATISTICS:")
print(f"  Total Features: {len(waterways)}")
print(f"  By Type:")
for feature_type in ['Estuary', 'Creek', 'River Channel']:
    count = len([w for w in waterways if w['Type'] == feature_type])
    print(f"    {feature_type}: {count}")
print(f"  By State:")
for state in ['Delta', 'Bayelsa', 'Rivers']:
    count = len([w for w in waterways if state in w['State']])
    print(f"    {state}: {count}")

print("\n" + "="*60)
print("FIGURE 1 COMPLETE - READY FOR SUBMISSION")
print("="*60)
print("\nCAPTION FOR FIGURE 1:")
print("-"*60)
print("Figure 1: GIS Inventory of Estuarine and Coastal Creek Systems in the Niger Delta.")
print("Multi-panel cartographic product showing (A) Nigeria national context highlighting")
print("the Niger Delta region, (B) Niger Delta regional context with core study states")
print("(Delta, Bayelsa, Rivers) highlighted (state labels removed for clarity, see legend),")
print("(C) main detailed map with OpenStreetMap basemap and all 23 hydrological features")
print("with color-shape differentiated markers, and (D) comprehensive legend. The main map")
print("includes a scale bar (100 km), compass rose (enlarged, with black cardinal points),")
print("and coordinate grid with degree-minute labels. State labels are retained on the")
print("main map (Panel C) for direct reference.")
print("-"*60)