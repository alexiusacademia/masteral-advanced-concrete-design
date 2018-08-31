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
for (i=1: 1: 4)
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

    
end






