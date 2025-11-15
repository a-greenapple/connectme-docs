#!/bin/bash

# Replace actual secrets with placeholders in documentation
find . -type f -name "*.md" -exec sed -i '' 's/88cebd3e-3fe7-426e-a351-915e2e96fa21/<REDACTED_CLIENT_ID>/g' {} \;
find . -type f -name "*.md" -exec sed -i '' 's/YOUR_CLIENT_SECRET_HERE/<REDACTED_CLIENT_SECRET>/g' {} \;

echo "✅ Secrets removed from documentation"
