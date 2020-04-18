from pathlib import Path

config_obj = {
    "env": "dev", # "production",
    "es_prod": "https://search-hk-demo-domain-cmwk32rmeh6dmoykeptm245iqa.eu-central-1.es.amazonaws.com",
    "dev_destination": f"{str(Path.home())}/programming_projects/knockhome/map-test-backend/mapTestBackend/polygons",
    "demo_destination": f"/var/www/hk_polygons",
}
