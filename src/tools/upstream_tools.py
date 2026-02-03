"""
Tools untuk Upstream Agent
Mengikuti prinsip MCP: tools yang dapat digunakan ulang dan terdokumentasi dengan baik
"""
from langchain_core.tools import tool
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random


@tool
def get_production_data(block_name: str) -> Dict[str, Any]:
    """
    Mengambil data produksi harian dari blok migas tertentu.
    
    Args:
        block_name: Nama blok migas (contoh: "Rokan", "Mahakam", "Cepu")
    
    Returns:
        Dictionary berisi data produksi minyak dan gas dalam BOPD (Barrel Oil Per Day)
        dan MMSCFD (Million Standard Cubic Feet per Day)
    
    Example:
        >>> get_production_data("Rokan")
        {
            "block": "Rokan",
            "date": "2026-02-02",
            "oil_production_bopd": 150000,
            "gas_production_mmscfd": 450,
            "status": "operational",
            "wells_active": 2500
        }
    """
    # Mock data - dalam implementasi real, ini akan query database atau API
    blocks_data = {
        "Rokan": {"oil": 150000, "gas": 450, "wells": 2500},
        "Mahakam": {"oil": 85000, "gas": 1200, "wells": 1800},
        "Cepu": {"oil": 35000, "gas": 180, "wells": 450},
    }
    
    block_info = blocks_data.get(
        block_name, 
        {"oil": 0, "gas": 0, "wells": 0}
    )
    
    return {
        "block": block_name,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "oil_production_bopd": block_info["oil"],
        "gas_production_mmscfd": block_info["gas"],
        "status": "operational" if block_info["oil"] > 0 else "unknown",
        "wells_active": block_info["wells"],
        "data_quality": "real-time"
    }


@tool
def get_lifting_schedule(block_name: str, days_ahead: int = 7) -> Dict[str, Any]:
    """
    Mengambil jadwal lifting (pengangkutan) minyak dari blok ke kilang/terminal.
    
    Args:
        block_name: Nama blok migas
        days_ahead: Jumlah hari ke depan untuk jadwal (default: 7)
    
    Returns:
        Dictionary berisi jadwal lifting untuk periode yang diminta
    
    Example:
        >>> get_lifting_schedule("Rokan", 3)
        {
            "block": "Rokan",
            "schedule": [
                {"date": "2026-02-03", "volume_barrels": 500000, "vessel": "MT XYZ Prime"},
                {"date": "2026-02-05", "volume_barrels": 500000, "vessel": "MT XYZ Excellence"}
            ]
        }
    """
    schedule = []
    base_date = datetime.now()
    
    # Generate mock schedule (setiap 2-3 hari ada lifting)
    for i in range(0, days_ahead, random.randint(2, 3)):
        schedule.append({
            "date": (base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "volume_barrels": random.randint(400000, 600000),
            "vessel": f"MT XYZ {random.choice(['Prime', 'Excellence', 'Victory', 'Glory'])}",
            "destination": random.choice(["Kilang Balongan", "Kilang Cilacap", "Terminal BBM Tanjung Priok"])
        })
    
    return {
        "block": block_name,
        "schedule_period_days": days_ahead,
        "schedule": schedule,
        "total_volume_barrels": sum(s["volume_barrels"] for s in schedule)
    }


@tool
def get_well_status(block_name: str, well_ids: List[str] = None) -> Dict[str, Any]:
    """
    Mengambil status operasional sumur-sumur di blok tertentu.
    
    Args:
        block_name: Nama blok migas
        well_ids: List ID sumur spesifik (opsional). Jika None, return semua sumur
    
    Returns:
        Dictionary berisi status detail sumur-sumur
    
    Example:
        >>> get_well_status("Rokan", ["RKN-001", "RKN-002"])
        {
            "block": "Rokan",
            "wells": [
                {"id": "RKN-001", "status": "producing", "production_bopd": 125},
                {"id": "RKN-002", "status": "maintenance", "downtime_hours": 48}
            ]
        }
    """
    # Mock data
    if not well_ids:
        well_ids = [f"{block_name[:3].upper()}-{str(i).zfill(3)}" for i in range(1, 6)]
    
    wells = []
    for well_id in well_ids:
        status = random.choice(["producing", "producing", "producing", "maintenance", "shut-in"])
        well_data = {
            "id": well_id,
            "status": status,
        }
        
        if status == "producing":
            well_data["production_bopd"] = random.randint(80, 200)
        elif status == "maintenance":
            well_data["downtime_hours"] = random.randint(24, 120)
            well_data["expected_restart"] = (datetime.now() + timedelta(hours=random.randint(12, 72))).isoformat()
        
        wells.append(well_data)
    
    return {
        "block": block_name,
        "total_wells_queried": len(wells),
        "wells": wells,
        "query_timestamp": datetime.now().isoformat()
    }


# Export all tools
upstream_tools = [
    get_production_data,
    get_lifting_schedule,
    get_well_status
]
