from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

def load_json_file(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
    
# Load tỉnh/thành phố
@app.get("/api/provinces")
def get_provinces():
    try:
        with open(os.path.join(DATA_DIR, "tinh_tp.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
        return list(data.values())
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Province data not found")

# Load quận/huyện theo mã tỉnh
@app.get("/api/districts/{province_code}")
def get_districts(province_code: str):
    path = os.path.join(DATA_DIR, "quan-huyen", f"{province_code}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="District data not found")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return list(data.values())

# Load xã/phường theo mã huyện
@app.get("/api/wards/{district_code}")
def get_wards(district_code: str):
    path = os.path.join(DATA_DIR, "xa-phuong", f"{district_code}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Ward data not found")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return list(data.values())


@app.get("/api/search")
def search_places(q: str = Query(..., min_length=2)):
    q_lower = q.lower()

    results = {
        "provinces": [],
        "districts": [],
        "wards": []
    }

    # Tìm tỉnh
    provinces = load_json_file(os.path.join(DATA_DIR, "tinh_tp.json")) or {}
    for p in provinces.values():
        if q_lower in p["name"].lower():
            results["provinces"].append(p)

    # Tìm huyện
    districts_dir = os.path.join(DATA_DIR, "quan-huyen")
    for filename in os.listdir(districts_dir):
        data = load_json_file(os.path.join(districts_dir, filename)) or {}
        for d in data.values():
            if q_lower in d["name"].lower():
                results["districts"].append(d)

    # Tìm xã
    wards_dir = os.path.join(DATA_DIR, "xa-phuong")
    for filename in os.listdir(wards_dir):
        data = load_json_file(os.path.join(wards_dir, filename)) or {}
        for w in data.values():
            if q_lower in w["name"].lower():
                results["wards"].append(w)

    return results


@app.get("/api/search/provinces")
def search_provinces(q: str = Query(..., min_length=2)):
    provinces = load_json_file(DATA_DIR / "tinh_tp.json") or {}
    q_lower = q.lower()
    return [p for p in provinces.values() if q_lower in p["name"].lower()]

@app.get("/api/search/districts")
def search_districts(q: str = Query(..., min_length=2)):
    q_lower = q.lower()
    results = []
    districts_dir = DATA_DIR / "quan-huyen"
    for file in districts_dir.glob("*.json"):
        data = load_json_file(file) or {}
        for d in data.values():
            if q_lower in d["name"].lower():
                results.append(d)
    return results

@app.get("/api/search/wards")
def search_wards(q: str = Query(..., min_length=2)):
    q_lower = q.lower()
    results = []
    wards_dir = DATA_DIR / "xa-phuong"
    for file in wards_dir.glob("*.json"):
        data = load_json_file(file) or {}
        for w in data.values():
            if q_lower in w["name"].lower():
                results.append(w)
    return results

@app.get("/api/search/full-address")
def search_full_address(q: str = Query(..., min_length=2)):
    q_lower = q.lower()

    # Load toàn bộ dữ liệu
    provinces = load_json_file(DATA_DIR / "tinh_tp.json") or {}
    provinces_map = {p["code"]: p["name"] for p in provinces.values()}
    # Tìm trong xã/phường
    results = []
    wards_dir = DATA_DIR / "xa-phuong"
    for ward_file in wards_dir.glob("*.json"):
        wards = load_json_file(ward_file) or {}
        for w in wards.values():
            if q_lower in w["name"].lower():
                district_code = w["parent_code"]
                # Load huyện
                district_file = DATA_DIR / "quan-huyen" / f"{district_code[:2]}.json"
                districts = load_json_file(district_file) or {}
                district = districts.get(district_code)
                if not district:
                    continue

                province_name = provinces_map.get(district["parent_code"], "Unknown")

                full = f"{w['name']}, {district['name']}, {province_name}"
                results.append({"level": "ward", "name": w["name"], "full_address": full})

    # Tìm trong quận/huyện
    districts_dir = DATA_DIR / "quan-huyen"
    for district_file in districts_dir.glob("*.json"):
        districts = load_json_file(district_file) or {}
        for d in districts.values():
            if q_lower in d["name"].lower():
                province_name = provinces_map.get(d["parent_code"], "Unknown")
                full = f"{d['name']}, {province_name}"
                results.append({"level": "district", "name": d["name"], "full_address": full})

    # Tìm trong tỉnh
    for p in provinces.values():
        if q_lower in p["name"].lower():
            full = p["name"]
            results.append({"level": "province", "name": p["name"], "full_address": full})

    return results