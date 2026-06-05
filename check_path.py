import sys
print("sys.path:")
for p in sys.path:
    print(f"  {p}")
print()
print("Checking for flask...")
try:
    import flask
    print(f"  Found flask at: {flask.__file__}")
except ImportError:
    print("  Flask NOT found in sys.path")

# Check user site-packages
import site
print(f"\nUser site-packages: {site.getusersitepackages()}")
import os
if os.path.exists(site.getusersitepackages()):
    print(f"  exists: True")
    flask_path = os.path.join(site.getusersitepackages(), 'flask')
    print(f"  flask dir exists: {os.path.exists(flask_path)}")
else:
    print(f"  exists: False")
