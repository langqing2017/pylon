//////////////////////////////////////////////////////////
/// ctpinfo tools
/// 20191222    langqing2017    创建该文件
////////////////////////////////////////////////////////////

#include <thread>
#include <chrono>
#include "CtpTradeInterface.h"

using namespace pylon;

#define USERNAME "005890"
#define PASSWORD "123456"
#define PRODUCT ""
#define AUTHCODE ""
#define BROKERID "9999"
#define TDFRONT "tcp://180.168.146.187:10101"

int main() {
    CCtpTradeInterface *trade = new CCtpTradeInterface(USERNAME, PASSWORD, PRODUCT, AUTHCODE, BROKERID, TDFRONT);
    trade->Init();
    std::this_thread::sleep_for(std::chrono::duration<int, std::ratio<1, 1000>>(10000));
}
