#!/bin/bash

# Redact all secret patterns
find . -type f -name "*.md" -exec sed -i '' 's/_zy8Q~_QT8FVJ1oiUYvBBSxxEDaRvytqTvO-2dfp/<REDACTED_SECRET>/g' {} \;
find . -type f -name "*.md" -exec sed -i '' 's/88cebd3e-3fe7-426e-a351-915e2e96fa21/<REDACTED_CLIENT_ID>/g' {} \;
find . -type f -name "*.md" -exec sed -i '' 's/client_secret = ".*"/client_secret = "<REDACTED>"/g' {} \;

echo "✅ All secrets redacted"
