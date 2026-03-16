#!/bin/bash
#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No argument supplied" >&2
    exit 1
fi

curl -fsS $1 | grep "moved here" | cut -d '"' -f 2
