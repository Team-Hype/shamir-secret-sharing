colored_echo() {
    local text="$1"
    local color="$2"

    case $color in
        red)
            echo -e "\033[31m$text\033[0m"
            ;;
        green)
            echo -e "\033[32m$text\033[0m"
            ;;
        yellow)
            echo -e "\033[33m$text\033[0m"
            ;;
        *)
            echo -e "$text"
            ;;
    esac
}