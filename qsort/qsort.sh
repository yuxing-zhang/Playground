#!/bin/bash
qs() {
    if (($1 >= $2)); then return; fi
    local i
    ((i = $1 + 1, j = $2))
    while true; do
        while ((i <= $2 && s[i] <= s[$1])); do ((i += 1)); done
        while ((j > $1 && s[j] >= s[$1])); do ((j -= 1)); done
        if ((i > j)); then break; fi
        ((t = s[i], s[i] = s[j], s[j] = t))
    done;
    ((t = s[$1], s[$1] = s[j], s[j] = t))
    qs $1 $((j - 1))
    qs $i $2 
}

s=()
i=0; while ((i < 10)); do s+=($(($RANDOM % 100))); ((i++)); done;
echo ${s[@]}
qs 0 $((${#s[@]} - 1))
echo ${s[@]}
