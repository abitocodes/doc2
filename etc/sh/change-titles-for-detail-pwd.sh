#!/bin/bash

# _results 디렉터리로 이동
cd _results

# crawled-links-title-2.json에서 각각의 'uppercase_transformed' 값을 추출하고 이를 이용하여 파일 이름을 변경
jq -r '.[] | select(.uppercase_transformed != "") | .uppercase_transformed + ".pdf"' ../crawled-links-title-2.json | while read new_filename; do
    # 해당 파일이 존재하는지 확인
    if [ -f "$new_filename" ]; then
        echo "$new_filename is already correctly named."
    else
        # last_segment 값을 사용하여 원래 파일을 찾아 이름을 변경
        original_filename=$(jq -r --arg filename "$new_filename" '.[] | select(.uppercase_transformed + ".pdf" == $filename) | .last_segment + ".pdf"' ../crawled-links-title-2.json)
        if [ -f "$original_filename" ]; then
            mv "$original_filename" "$new_filename"
            echo "Renamed $original_filename to $new_filename"
        else
            echo "No file found to rename for $new_filename"
        fi
    fi
done
