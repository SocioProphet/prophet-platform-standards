.PHONY: validate multidomain-geospatial-validate

validate:
	./.venv/bin/python tools/validate_multidomain_geospatial_registry.py 2>/dev/null || python3 tools/validate_multidomain_geospatial_registry.py

multidomain-geospatial-validate:
	./.venv/bin/python tools/validate_multidomain_geospatial_registry.py 2>/dev/null || python3 tools/validate_multidomain_geospatial_registry.py
