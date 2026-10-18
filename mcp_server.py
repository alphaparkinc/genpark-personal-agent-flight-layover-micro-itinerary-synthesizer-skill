#!/usr/bin/env python3
import json
import sys
from client import PersonalAgentLayoverItinerarySynthesizer

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        synth = PersonalAgentLayoverItinerarySynthesizer()
        res = synth.synthesize_layover_tour("HND", 360) # 6 hours layover at Haneda
        assert res["itinerary_status"] == "SAFE_CITY_TOUR_DISPATCHED"
        assert res["net_usable_exploration_minutes"] > 100
        assert len(res["recommended_stops"]) >= 1
        print(f"[TEST PASS] Layover Itinerary: {res['city']} ({res['net_usable_exploration_minutes']} mins usable)")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-layover-synthesizer", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "synthesize_layover_tour", "description": "Synthesize safe flight layover micro-itinerary with zero miss-risk"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                synth = PersonalAgentLayoverItinerarySynthesizer()
                out = synth.synthesize_layover_tour(args.get("airport_code", "SIN"), int(args.get("layover_minutes", 300)), args.get("traveler_preferences"))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
