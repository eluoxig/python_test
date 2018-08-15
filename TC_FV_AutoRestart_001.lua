require("C:/AN20K/Testing/lib/funcs_and_signals")
require('C:/AN20K/Testing/lib/e4_common')


	local case = "TC_FV_AutoRestart_001"

	Logger.file = case .. ".log"
	Logger.level = 2
	Logger:clear()
	
	FlushData()
	function uptimeToSeconds(str)
		local seconds = 0
		local days, rest = str:match("(%d+)[^0-9]-day.-([0-9:]+)")
		if not (days and rest) then
			Logger:error("Invalid uptime string '" .. str .. "', unable to convert to seconds")
		end

		seconds = seconds + tonumber(days) * 86400
		mult = 60 * 60
		for m in rest:gmatch("(%d+)") do
			seconds = seconds + tonumber(m) * mult
			mult = mult / 60
		end

		return seconds
	end

		-- Test start --

	function start_timer()
		Logger:info("this is to start 48h timer.")
		Sleep(1000)
		Logger:log(motherIpcCommunicator:execute("fmgr local raise 5010", {collectOutput=true}))
		Sleep(1000)
		Logger:log("Remove the CPRI cable now. You have 30 seconds.")
		Logger:log(motherIpcCommunicator:execute("stop RICR_sup_link_1;hwyFpga w 0x22E 0x3 0x0", {collectOutput=true}))
		Sleep(2*60*1000)
		Logger:info("CPRI link should be going up now, sleeping for 1 second more.")
		Sleep(10000)
		
		if(check_auto_state()) then
			Logger:info("now state is right")
		end
		
	end


	function trim(s)   
		return (string.gsub(s, "^%s*(.-)%s*$", "%1"))  
	end  

	function  check_auto_state()
		local result = true
	
		local recovery_info= motherIpcCommunicator:execute("fmgr recovery info ", {collectOutput=true}).data
	
		local state= trim(string.sub(recovery_info,55,57))


		if state == "no" then
			Logger:info("auto restart suppression state is : "..state)
			result = false
		elseif state =="yes" then
			Logger:info("auto restart suppression state is : "..state)
		end
		return result
	end 

	function uptime()
		local uptime = motherIpcCommunicator:execute("uptime", {collectOutput=true}).data
		print("start uptime = ", uptime)
		Logger:info("start uptime  "..uptime..".......")
		local rutime = uptimeToSeconds(uptime)
		print("start_rutime = ", rutime)
		
		return rutime
	end
		--48 hours suppression timer
	local result = false;
	local tolerance = 10
	
	-- Sleep(1000)
	--how to check the alarm status
	Logger:info(" record time before cpri link down ")
	
	local start_rutime = uptime()
	local start_systime=os.time()
	Logger:info("start systime  "..start_systime)
	
	
	Sleep(1000)
	if not check_auto_state() then
		Logger:info("please execute state to yes")
		start_timer()
	end
	Sleep(1000)
	
	
	local end2_systime = os.time()
	Logger:info("cpri up end systime  "..end2_systime.." ")
	local end2_rutime=uptime()
	
	---second 
	Sleep(1000)
	
	local ru_diff= end2_rutime- start_rutime
	local sys_diff= end2_systime-start_systime
	Logger:info("ru_diff is "..ru_diff)
	Logger:info("sys_diff is "..sys_diff)
	
	if (sys_diff-ru_diff) > tolerance then
		Logger:log("RU restart ")
		result = true
	else
		Logger:log("RU didn't restart")
	end
	
	
	local suc = result and "PASS" or "FAIL"
	Logger:log(" == TEST CASE " .. case .. ": " .. suc .. " == ")
	