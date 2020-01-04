/////////////////////////////////////////////////////////////////////////
///CtpTradeInterface
///20191222    langqing2017    Create
/////////////////////////////////////////////////////////////////////////

#include <thread>
#include "utils.h"
#include "CtpTradeInterface.h"

using namespace pylon;

void CCtpTradeInterface::Init()
{
    std::cerr << "CtpTradeInterface正在初始化..." << std::endl;

    m_pcTraderApi = CThostFtdcTraderApi::CreateFtdcTraderApi("./Log/");

    //Connect Front
    m_pcTraderApi->RegisterSpi(this);
    m_pcTraderApi->RegisterFront((char *)m_strTradeFrontAddress.c_str());
    m_pcTraderApi->SubscribePublicTopic(THOST_TERT_RESTART);
    m_pcTraderApi->SubscribePrivateTopic(THOST_TERT_RESTART);
    m_pcTraderApi->Init();
}

void CCtpTradeInterface::OnFrontConnected()
{
    std::cerr << "CtpTradeInterface交易前置连接成功." << std::endl;

    if(m_bLoginFailed == false) {
        if(m_strAuthCode == "" || m_strProduct == "") {
            CThostFtdcReqUserLoginField req;
            memset(&req, 0, sizeof(req));
            strncpy(req.BrokerID, m_strBrokerId.c_str(), sizeof(req.BrokerID));
            strncpy(req.UserID, m_strUsername.c_str(), sizeof(req.UserID));
            strncpy(req.Password, m_strPassword.c_str(), sizeof(req.Password));
            int iResult = m_pcTraderApi->ReqUserLogin(&req, ++m_iRequestSeq);
            if (0 != iResult) {
                std::cerr << "CtpTradeInterface发送用户登录失败!（错误码：" << iResult << ")." << std::endl;
                return;
            }
            std::cerr << "CtpTradeInterface发送用户(" << m_strUsername << ")登录成功." << std::endl;
        }
        else {
            //auth first
            CThostFtdcReqAuthenticateField reqAuth;
            memset(&reqAuth, 0, sizeof(CThostFtdcReqAuthenticateField));
            strncpy(reqAuth.BrokerID, m_strBrokerId.c_str(), sizeof(reqAuth.BrokerID));
            strncpy(reqAuth.UserID, m_strUsername.c_str(), sizeof(reqAuth.UserID));
            strncpy(reqAuth.UserProductInfo, m_strProduct.c_str(), sizeof(reqAuth.UserProductInfo));
            strncpy(reqAuth.AuthCode, m_strAuthCode.c_str(), sizeof(reqAuth.AuthCode));
            int iResult = m_pcTraderApi->ReqAuthenticate(&reqAuth, ++m_iRequestSeq);

            if (0 != iResult) {
                std::cerr << "CtpTradeInterface发送认证请求失败！（" << iResult << ")" << std::endl;
                return;
            }
            std::cerr << "CtpTradeInterface发送认证请求成功." << std::endl;
        }
    }
}

void CCtpTradeInterface::OnFrontDisconnected(int nReason)
{
    std::cerr << "CtpTradeInterface连接中断!(错误码：" << nReason << ")" << std::endl;
}

void CCtpTradeInterface::OnRspAuthenticate(CThostFtdcRspAuthenticateField *pRspAuthenticateField, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
    if (NULL != pRspInfo && 0 != pRspInfo->ErrorID) {
        std::cerr << "CtpTradeInterface(" << m_strUsername << ")认证失败（" << pRspInfo->ErrorID << ")." << std::endl;
        m_bLoginFailed = true;
        return;
    }
    else {
        std::cerr << "CtpTradeInterface认证成功." << std::endl;
    }

    //等待1000ms
    std::this_thread::sleep_for(std::chrono::duration<int, std::ratio<1, 1000>>(1000));

    CThostFtdcReqUserLoginField req;
    memset(&req, 0, sizeof(req));
    strncpy(req.BrokerID, m_strBrokerId.c_str(), sizeof(req.BrokerID));
    strncpy(req.UserID, m_strUsername.c_str(), sizeof(req.UserID));
    strncpy(req.Password, m_strPassword.c_str(), sizeof(req.Password));
    int iResult = m_pcTraderApi->ReqUserLogin(&req, ++m_iRequestSeq);
    if (0 != iResult) {
        std::cerr << "CtpTradeInterface发送用户登录失败!（错误码：" << iResult << ")." << std::endl;
    }
    std::cerr << "CtpTradeInterface发送用户(" << m_strUsername << ")登录成功." << std::endl;
}

///登录请求响应
void CCtpTradeInterface::OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
    if (NULL != pRspInfo && 0 != pRspInfo->ErrorID) {
        std::cerr << "CtpTradeInterface(" << m_strUsername << ")登录失败（" << pRspInfo->ErrorID << ")." << std::endl;
        m_bLoginFailed = true;
        return;
    }
    else {
        m_dtTradingDay = CroParseDateNoDash(pRspUserLogin->TradingDay);     //YYYYMMDD
        m_iFrontId = pRspUserLogin->FrontID;
        m_iSessionId = pRspUserLogin->SessionID;
        std::cerr << "CtpTradeInterface登录成功(" << CroDateTimeFormat(m_dtTradingDay) << ")." << std::endl;
    }

    //等待1000ms
    std::this_thread::sleep_for(std::chrono::duration<int, std::ratio<1, 1000>>(1000));

    CThostFtdcSettlementInfoConfirmField reqConfirm;
    memset(&reqConfirm, 0, sizeof(CThostFtdcSettlementInfoConfirmField));
    strncpy(reqConfirm.BrokerID, m_strBrokerId.c_str(), sizeof(reqConfirm.BrokerID));
    strncpy(reqConfirm.InvestorID, m_strUsername.c_str(), sizeof(reqConfirm.InvestorID));
    int iResult = m_pcTraderApi->ReqSettlementInfoConfirm(&reqConfirm, ++m_iRequestSeq);

    if (0 != iResult) {
        std::cerr << "CtpTradeInterface发送投资者结算结构确认失败！（" << iResult << ")" << std::endl;
        return;
    }
    std::cerr << "CtpTradeInterface发送投资者结算结构确认成功." << std::endl;
}

///投资者结算结果确认响应
void CCtpTradeInterface::OnRspSettlementInfoConfirm(CThostFtdcSettlementInfoConfirmField *pSettlementInfoConfirm, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
    if (NULL != pRspInfo && 0 != pRspInfo->ErrorID) {
        std::cerr << "CtpTradeInterface投资者结算结构确认失败(" << pRspInfo->ErrorID << ")." << std::endl;
        return;
    }
    std::cerr << "CtpTradeInterface投资者结算结构确认成功." << std::endl;

    //Trader初始化完毕
    std::cerr << "CtpTradeInterface初始化完毕！" << std::endl;

    //查询Product
    CThostFtdcQryProductField req;
    memset(&req, 0, sizeof(CThostFtdcQryProductField));
    int iResult = m_pcTraderApi->ReqQryProduct(&req, ++m_iRequestSeq);

    if (0 != iResult) {
        std::cerr << "CtpTradeInterface发送产品查询失败！（" << iResult << ")" << std::endl;
        return;
    }
    std::cerr << "CtpTradeInterface发送产品查询成功." << std::endl;
}

///请求查询产品响应
void CCtpTradeInterface::OnRspQryProduct(CThostFtdcProductField* pProduct, CThostFtdcRspInfoField* pRspInfo, int nRequestID, bool bIsLast) {
    if (NULL != pRspInfo && 0 != pRspInfo->ErrorID) {
        std::cerr << "CtpTradeInterface产品查询失败(" << pRspInfo->ErrorID << ")." << std::endl;
        return;
    }

    std::cout << pProduct->ExchangeID << ", " << pProduct->ProductID << ", " << pProduct->ProductName << ", " 
                << pProduct->PriceTick << ", " << pProduct->VolumeMultiple << std::endl;

    if (bIsLast) {
        std::cerr << "CtpTradeInterface产品查询成功." << std::endl;
    }
}
