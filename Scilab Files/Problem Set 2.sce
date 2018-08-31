// Function to get centroid of a t-beam
function centroid = centroidOfTBeam(bf, tf, bw, y)
    if (y <= tf) then
        centroid = y / 2
    else
        area_total = bf * tf + bw * (y - tf)
        moment_area = bf * tf * tf / 2 + ..
                      bw * (y - tf) * ((y - tf) / 2 + tf)
        centroid = moment_area / area_total
    end
endfunction

// Function to calculate total area of t-beam
function totalArea = tbeamArea(bf, tf, bw, y)
    if (y <= tf) then
        totalArea = bf * y
    else
        totalArea = bf * tf + bw * (y - tf)
    end
endfunction

student_number = [3 3 8]          // Student number to be reversed
d = 435
bw = 250
tf = 125
ϵcu = 0.003
Es = 200000
fc_base = 28                        // Basis for calculating β1

// Reverse the student number then convert to appropriate format
student_number_reversed = "."
for i = size(student_number, "c"): -1: 1 
    student_number_reversed = student_number_reversed + string(student_number(1, i))
end

// Convert to number
student_number_reversed = strtod(student_number_reversed)

// Factor for calculating flange width
α = 10 + 10 * student_number_reversed

// Calculate for b then round to the nearest 25mm
bf = bw + α * tf
bf = round(bf / 100 * 4) / 4 * 100

fcPrime = [20 40 20 40]
fy = [300 300 400 400]
β1 = []

// Calculate for each β1
for (i = 1: 1: size(fcPrime, "c"))
    if fcPrime(1, i) <= fc_base then
        β1(1, i) = 0.85
    else
        β1(1, i) = 0.85 - (0.05 / 7)*(fcPrime(1, i) - fc_base)
    end
end

// -------------------------------------
// Start of problem main calculation
// -------------------------------------
result = list()
for (i = 1: 1: 4)
    // Calculate balanced value for 'c'
    c_bal = 600 * d / (600 + fy(1, i))

    // Balanced equivalent compression block height
    a_bal = β1(1, i) * c_bal

    // Web component of the compression, z
    z_bal = 0
    if (a_bal > tf) then
        z_bal = a_bal - tf
    else
        z_bal = 0
    end

    // Balanced equation
    // Asb.fy = 0.85 f'c.bf.tf + 0.85f'c.bw.z
    As_bal = (0.85 * fcPrime(1, i) * bf * tf + 0.85 * fcPrime(1, i) * bw * z_bal) / fy(1, i)
    
    As_limit = 2 * As_bal
    
    As_trial = 100
    Mmax = 0.0
    
    dataColumn = [0, 0]
    row_ctr = 2
    while (As_trial <= As_limit)
        a = 0
        c = a / β1(1, i)
        As_calc = 0
        fs = 0.0
        fs_actual = 0.0
        
        while (As_calc < As_trial)
            c = a / β1(1, i)
            fs = 600 * (d - c) / c
            fs_actual = fs
            if (fs >= fy(1, i)) then
                fs = fy(1, i)
            end
            Ac = tbeamArea(bf, tf, bw, a)
            
            As_calc = 0.85 * fcPrime(1, i) * Ac / fs
            a = a + 0.2
        end
        
        // Calculate for the strain in concrete
        ϵc = (fs/Es) / (d-c) * c
        
        // Calculate moment
        Mn = As_calc * fs * (d - centroidOfTBeam(bf, tf, bw, a))

        As_trial = As_trial + 100
        
        dataColumn(row_ctr, 1) = As_calc
        dataColumn(row_ctr, 2) = Mn
        
        row_ctr = row_ctr + 1
    end
    
    result($+1) = dataColumn
end

plot(result(1), 'rs')
plot(result(2), 'bs')
plot(result(3), 'gs')
plot(result(4), 'ms')
xtitle("Moment Capacity Curve")
xlabel("Steel Area")
ylabel("Moment Capacity")


