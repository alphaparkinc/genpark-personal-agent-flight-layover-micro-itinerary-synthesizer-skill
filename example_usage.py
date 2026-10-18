from client import PersonalAgentLayoverItinerarySynthesizer

def main():
    synth = PersonalAgentLayoverItinerarySynthesizer()
    res = synth.synthesize_layover_tour("AMS", 420)
    print("--- Flight Layover Concierge ---")
    print(f"Airport: {res['airport']} ({res['city']}) | Total Layover: {res['total_layover_minutes']}m")
    print(f"Net City Time: {res['net_usable_exploration_minutes']}m | Status: {res['itinerary_status']}")
    print(f"Advice: {res['safety_advice']}")
    for st in res['recommended_stops']:
        print(f"* Step {st.get('step', 1)}: {st['attraction_name']} ({st['allocated_minutes']}m)")

if __name__ == "__main__":
    main()
