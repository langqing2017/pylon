//////////////////////////////////////////////////////////
/// utils
/// 20191222    langqing2017    Create
////////////////////////////////////////////////////////////

#pragma once

#include <cstring>
#include <chrono>
#include <string>

namespace pylon {
    typedef std::chrono::time_point<std::chrono::system_clock, std::chrono::system_clock::duration> csc_tp;

    // return time point
    // month: 0-11
    inline csc_tp GenTimePoint(int year, int month, int day, int hour, int minute, int second) {
        tm target_tm;
        memset(&target_tm, sizeof(tm), 0);
        target_tm.tm_year = year - 1900;
        target_tm.tm_mon = month;
        target_tm.tm_mday = day;
        target_tm.tm_hour = hour;
        target_tm.tm_min = minute;
        target_tm.tm_sec = second;
        time_t target_time = mktime(&target_tm);

        //
        csc_tp target_tp = std::chrono::system_clock::from_time_t(target_time);
        return target_tp;
    }

    // parse time string YYYYMMDD
    inline csc_tp CroParseDateNoDash(std::string s) {
        if (s.size() != 8) {
            return csc_tp::min();
        }
        int year = atoi(s.substr(0, 4).c_str());
        int month = atoi(s.substr(4, 2).c_str());
        int day = atoi(s.substr(6, 2).c_str());
        return GenTimePoint(year, month - 1, day, 0, 0, 0);
    }

    // return time string yyyymmdd HH:MM:SS.XXXXXX
    inline std::string CroDateTimeFormat(const csc_tp& t) {
        uint64_t timestamp = std::chrono::duration_cast<std::chrono::microseconds>(t.time_since_epoch()).count();
        time_t tt = static_cast<uint64_t>(timestamp * 0.000001);

#ifndef LINUX
        std::tm gmtime;
        localtime_s(&gmtime, &tt);
#else
        std::tm gmtime;
        localtime_r(&tt, &gmtime);
#endif

        char buffer[32] = { 0 };
        char microseconds[10] = { 0 };
        strftime(buffer, sizeof(buffer), "%Y%m%d %H:%M:%S", &gmtime);
        snprintf(microseconds, sizeof(microseconds), ".%06llu ", timestamp % 1000000);

        std::string time;
        time.append(buffer).append(microseconds);
        return time;
    }

}
