# CMakeList.txt: CS3201_socketprogramming 的 CMake 專案，在此包含來源及定義
# 專案專屬邏輯。
#

# 將來源新增到此專案的可執行檔。
add_executable (CS3201_socketprogramming "CS3201_socketprogramming.cpp" "CS3201_socketprogramming.h")

find_package(sockpp REQUIRED)

target_link_libraries(CS3201_socketprogramming Sockpp::sockpp)

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET CS3201_socketprogramming PROPERTY CXX_STANDARD 20)
endif()

# TODO: 新增測試，並視需要安裝目標。
