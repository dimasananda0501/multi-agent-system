"""
Tools untuk Logistics Agent
Menangani tracking kapal tanker dan data cuaca untuk pengiriman
"""
from langchain_core.tools import tool
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random


@tool
def track_vessel(vessel_name: str) -> Dict[str, Any]:
    """
    Melacak posisi dan status kapal tanker secara real-time.
    
    Args:
        vessel_name: Nama kapal (contoh: "MT XYZ Prime")
    
    Returns:
        Dictionary berisi koordinat, kecepatan, rute, dan ETA
    
    Example:
        >>> track_vessel("MT XYZ Prime")
        {
            "vessel_name": "MT XYZ Prime",
            "current_position": {"latitude": -6.123, "longitude": 106.456},
            "speed_knots": 12.5,
            "eta_hours": 18
        }
    """
    # Mock vessel data
    routes = {
        "MT XYZ Prime": {
            "origin": "Dumai Terminal",
            "destination": "Kilang Balongan",
            "current_location": "Selat Sunda",
            "position": {"latitude": -6.123, "longitude": 106.456}
        },
        "MT XYZ Excellence": {
            "origin": "Balikpapan Terminal",
            "destination": "Kilang Cilacap",
            "current_location": "Selat Makassar",
            "position": {"latitude": -3.456, "longitude": 118.789}
        }
    }
    
    vessel_data = routes.get(
        vessel_name,
        {
            "origin": "Unknown",
            "destination": "Unknown",
            "current_location": "Unknown",
            "position": {"latitude": 0, "longitude": 0}
        }
    )
    
    # Simulasi kondisi cuaca yang mempengaruhi kecepatan
    weather_impact = random.choice([0, 0, -2, -4, -6])  # Mostly normal, kadang lambat
    base_speed = 14
    
    return {
        "vessel_name": vessel_name,
        "origin": vessel_data["origin"],
        "destination": vessel_data["destination"],
        "current_location": vessel_data["current_location"],
        "current_position": vessel_data["position"],
        "speed_knots": base_speed + weather_impact,
        "status": "on_schedule" if weather_impact >= -2 else "delayed",
        "cargo_volume_barrels": random.randint(450000, 550000),
        "eta_hours": random.randint(12, 30),
        "timestamp": datetime.now().isoformat()
    }


@tool
def get_weather_forecast(location: str, hours_ahead: int = 24) -> Dict[str, Any]:
    """
    Mengambil prakiraan cuaca untuk rute pelayaran.
    
    Args:
        location: Nama lokasi/selat (contoh: "Selat Sunda", "Selat Makassar")
        hours_ahead: Jam ke depan untuk prakiraan (default: 24)
    
    Returns:
        Dictionary berisi kondisi cuaca dan rekomendasi navigasi
    
    Example:
        >>> get_weather_forecast("Selat Sunda", 24)
        {
            "location": "Selat Sunda",
            "wave_height_meters": 2.5,
            "wind_speed_knots": 18,
            "risk_level": "moderate"
        }
    """
    # Mock weather data
    wave_height = random.uniform(0.5, 4.5)
    wind_speed = random.uniform(8, 35)
    
    # Determine risk level
    if wave_height > 3.5 or wind_speed > 30:
        risk_level = "high"
        navigation_advice = "Consider delaying departure. High waves and strong winds."
    elif wave_height > 2.0 or wind_speed > 20:
        risk_level = "moderate"
        navigation_advice = "Proceed with caution. Expect speed reduction."
    else:
        risk_level = "low"
        navigation_advice = "Normal sailing conditions."
    
    return {
        "location": location,
        "forecast_period_hours": hours_ahead,
        "wave_height_meters": round(wave_height, 1),
        "wind_speed_knots": round(wind_speed, 1),
        "visibility_km": random.randint(5, 20),
        "risk_level": risk_level,
        "navigation_advice": navigation_advice,
        "forecast_timestamp": datetime.now().isoformat(),
        "valid_until": (datetime.now() + timedelta(hours=hours_ahead)).isoformat()
    }


@tool
def get_delivery_status(shipment_id: str) -> Dict[str, Any]:
    """
    Mengambil status pengiriman end-to-end dari source ke destination.
    
    Args:
        shipment_id: ID pengiriman unik
    
    Returns:
        Dictionary berisi detail lengkap status pengiriman
    
    Example:
        >>> get_delivery_status("SHP-2026-001")
        {
            "shipment_id": "SHP-2026-001",
            "status": "in_transit",
            "progress_percentage": 65
        }
    """
    statuses = ["scheduled", "loading", "in_transit", "arrived", "discharged"]
    current_status = random.choice(statuses)
    
    status_progress = {
        "scheduled": 0,
        "loading": 20,
        "in_transit": random.randint(30, 80),
        "arrived": 90,
        "discharged": 100
    }
    
    return {
        "shipment_id": shipment_id,
        "status": current_status,
        "progress_percentage": status_progress[current_status],
        "origin_block": random.choice(["Rokan", "Mahakam", "Cepu"]),
        "destination_refinery": random.choice(["Kilang Balongan", "Kilang Cilacap", "Kilang Balikpapan"]),
        "vessel_assigned": f"MT XYZ {random.choice(['Prime', 'Excellence'])}",
        "volume_barrels": random.randint(450000, 550000),
        "departure_date": (datetime.now() - timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d"),
        "estimated_arrival": (datetime.now() + timedelta(hours=random.randint(6, 48))).isoformat(),
        "last_updated": datetime.now().isoformat()
    }


# Export all tools
logistics_tools = [
    track_vessel,
    get_weather_forecast,
    get_delivery_status
]
