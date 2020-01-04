/////////////////////////////////////////////////////////////////////////
/// CtpTradeInterface
/// 20191222    langqing2017    Create
/////////////////////////////////////////////////////////////////////////

#pragma once

#include <iostream>
#include <string>
#include <mutex>
#include "utils.h"
#include "ThostFtdcTraderApi.h"

namespace pylon {

    class CCtpTradeInterface: public CThostFtdcTraderSpi {
    public:
        //
        CCtpTradeInterface(std::string v_strUsername, std::string v_strPassword, std::string v_strProduct, std::string v_strAuthCode, std::string v_strBrokerId, std::string v_strTradeFrontAddress)
            : m_strUsername(v_strUsername), m_strPassword(v_strPassword), m_strProduct(v_strProduct), m_strAuthCode(v_strAuthCode),
            m_strBrokerId(v_strBrokerId), m_strTradeFrontAddress(v_strTradeFrontAddress), m_iRequestSeq(1) {
            printf("Username: %s\nProduct: %s\nAuthCode: %s\nBrokerId: %s\nTradeFrontAddress: %s\n",
                    m_strUsername.c_str(), m_strProduct.c_str(),
                    m_strAuthCode.c_str(), m_strBrokerId.c_str(), m_strTradeFrontAddress.c_str());
            m_nOrderRef = 1;
            m_bLoginFailed = false;
        }

        //
        virtual ~CCtpTradeInterface() {}

    public:
        //
        void Init();

    //---------------ThostFtdcTraderSpi------------------//
    public:
        ///
        virtual void OnFrontConnected();

        ///
        virtual void OnFrontDisconnected(int nReason);

        ///
        virtual void OnRspAuthenticate(CThostFtdcRspAuthenticateField *pRspAuthenticateField, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

        ///
        virtual void OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

        ///
        virtual void OnRspSettlementInfoConfirm(CThostFtdcSettlementInfoConfirmField *pSettlementInfoConfirm, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast);

        ///请求查询产品响应
        virtual void OnRspQryProduct(CThostFtdcProductField* pProduct, CThostFtdcRspInfoField* pRspInfo, int nRequestID, bool bIsLast);

        ///
        virtual void OnRspError(CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
            if (NULL != pRspInfo && 0 != pRspInfo->ErrorID) {
                std::cerr << "CtpTradeInterface错误(" << pRspInfo->ErrorID << ").";
                return;
            }
        }

    private:
        std::string m_strUsername;
        std::string m_strPassword;
        std::string m_strProduct;
        std::string m_strAuthCode;
        std::string m_strBrokerId;
        std::string m_strTradeFrontAddress;

    private:
        //
        long GetNextOrderRef() {
            long nRet = 0;
            std::lock_guard<std::mutex> lock(m_mtxOrderRef);
            nRet = ++m_nOrderRef;
            return nRet;
        }

    private:
        bool m_bLoginFailed;    //是否登陆失败
        int m_iRequestSeq;        //当前请求序号
        csc_tp m_dtTradingDay;    //当前交易日
        int m_iFrontId;            //当前连接的FrontId
        int m_iSessionId;        //当前连接的SessionId

        //OrderRef
        std::mutex m_mtxOrderRef;
        long m_nOrderRef;

        //API对象
        CThostFtdcTraderApi* m_pcTraderApi;
    };

}
