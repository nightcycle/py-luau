source env/Scripts/Activate
find src -type f -name "*.pyi" -delete
stubgen src/luau -o src
