"""
Personal Agent Layover Micro-Itinerary Synthesizer (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
from typing import Dict, Any, List, Optional

class PersonalAgentLayoverItinerarySynthesizer:
    AIRPORT_CITY_HUBS = {
        "HND": {"city": "Tokyo", "train_mins": 25, "attractions": ["Asakusa Sensoji Temple", "Tsukiji Outer Market", "Ginza Stroll"]},
        "SIN": {"city": "Singapore", "train_mins": 30, "attractions": ["Jewel Changi Vortex", "Marina Bay Sands", "Gardens by the Bay"]},
        "AMS": {"city": "Amsterdam", "train_mins": 18, "attractions": ["Rijksmuseum Area", "Canal Ring Cruise", "Jordaan Quarter"]},
        "ICN": {"city": "Seoul", "train_mins": 45, "attractions": ["Incheon Songdo Central Park", "Hongdae Food Alley"]}
    }

    def __init__(self, synthesizer_name: str = "GenPark-Layover-Concierge"):
        self.synthesizer_name = synthesizer_name

    def synthesize_layover_tour(self, airport_code: str, layover_minutes: int, traveler_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        code = airport_code.upper()
        hub = self.AIRPORT_CITY_HUBS.get(code, {"city": "Transit City", "train_mins": 30, "attractions": ["Airport Transit Lounge", "City Center Plaza"]})
        
        # Fixed mandatory safety buffers:
        # 1. Deplane + Customs/Immigration exit: 45 mins
        # 2. Return security screening + Boarding gate buffer: 90 mins
        # 3. Roundtrip transit to city: train_mins * 2
        deplane_customs = 45
        security_boarding = 90
        roundtrip_transit = hub["train_mins"] * 2
        
        usable_minutes = layover_minutes - (deplane_customs + security_boarding + roundtrip_transit)
        
        stops = []
        if usable_minutes < 60:
            status = "AIRPORT_BOUND_EXPLORATION_RECOMMENDED"
            advice = f"Layover ({layover_minutes}m) is too tight for safe city transit. Enjoy premium airport amenities at {code}."
            stops.append({"name": f"{code} Jewel / Terminal Oasis", "duration_mins": min(90, layover_minutes - 90), "type": "AIRPORT_AMENITY"})
        else:
            status = "SAFE_CITY_TOUR_DISPATCHED"
            advice = f"Safe {usable_minutes} mins available in {hub['city']}. Guaranteed return 90m before departure."
            
            time_per_stop = 60
            max_stops = max(1, min(len(hub["attractions"]), usable_minutes // time_per_stop))
            for i in range(max_stops):
                stops.append({
                    "step": i + 1,
                    "attraction_name": hub["attractions"][i],
                    "allocated_minutes": time_per_stop,
                    "city": hub["city"]
                })
                
        return {
            "synthesizer": self.synthesizer_name,
            "airport": code,
            "city": hub["city"],
            "total_layover_minutes": layover_minutes,
            "net_usable_exploration_minutes": max(0, usable_minutes),
            "safety_buffer_minutes": deplane_customs + security_boarding,
            "itinerary_status": status,
            "recommended_stops": stops,
            "safety_advice": advice,
            "verdict": "LAYOVER_ITINERARY_SYNTHESIZED"
        }
