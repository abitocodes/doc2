#!/bin/bash

# _results 디렉터리로 이동
cd _results

# crawled-links-title-2.json에서 모든 'uppercase_transformed' 값을 추출
uppercase_transformed_list=$(jq -r '.[] | select(.uppercase_transformed != "") | .uppercase_transformed + ".pdf"' ../crawled-links-title-2.json)

# _results 폴더의 모든 파일을 확인
for file in *.pdf; do
    # 파일 이름이 uppercase_transformed_list에 없다면 메시지 출력
    if ! grep -q "$file" <<< "$uppercase_transformed_list"; then
        echo "No match found for $file in uppercase_transformed values."
    fi
done
