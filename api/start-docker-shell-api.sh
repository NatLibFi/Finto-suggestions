#!/bin/bash

read -p "You are entering the Docker Shell - if ok press 'y': " answer
case ${answer:0:1} in
    y|Y )
        docker exec -it finto-suggestions_api_1 sh
        # docker exec -it 8b4e6113eb34_finto-suggestions_api_1 sh
    ;;
    * )
        echo "Maybe next time.."
    ;;
esac