function load_iat(file)
  lines = {}
  local f = io.open(file, "r")
  if f~=nil then
    io.close(f)
  else
    return lines
  end
  for line in io.lines(file) do
    if not (line == '') then
      lines[#lines+1] = tonumber(line)
    end
  end
  print(lines)
  return lines
end

iat1 = load_iat("/home/labtlc/openfaas_k3s_rl/iat_1_B.txt")


local counteriat=0

function delay()
  iat = iat1[counteriat]
  counteriat = counteriat + 1
  return tonumber(iat)
end

local counter = 1

function response()
  if (counter == 1819) then
    print("All requests sent")
    wrk.thread:stop()
  end
  counter = counter+1
end

done = function(summary, latency, requests)
   local filelat = assert(io.open("latreport1.csv", "w"))
   filelat:write('Perc')
   filelat:write('\n')
   filelat:write(latency:percentile(99.0))
   filelat:close()
   local file = assert(io.open("report1.csv", "w"))
   file:write('Min latency'..","..'Avg latency'..","..'Max latency'..","..'Stdev'..","..'Perc')
   file:write('\n')
   file:write(latency.min ..","..latency.mean..","..latency.max..","..latency.stdev..","..latency:percentile(99.0))
   local summaryfile = assert(io.open("summary1.csv","w"))
   summaryfile:write('Total requests timeouts', 'Total errors')
   summaryfile:write('\n')
   summaryfile:write(summary["errors"]["timeout"],  summary["errors"]["status"])
   summaryfile:close()
end




