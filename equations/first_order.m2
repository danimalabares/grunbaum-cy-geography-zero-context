-- Generated exactly from the frozen zero-context source.
S = QQ[a,b,c,d,e,f,g,h,q];
f0List = {a*b*f,a*b*g,a*b*h,a*c*g,a*c*h,a*d*h,b*d*f,b*d*g,b*e*g,c*d*e,c*e*g,c*e*h,c*f*h,d*e*f,d*f*h,e*f*g};
g1List = {10*a^2*c+a*c*e+2*b*c*e+3*c^2*e+4*c*e^2+5*c*e*f+9*e*f^2+8*f^2*h,8*a*d*e+8*f*g*h,8*b^2*d+9*b*d*e+9*e*f*h+8*f*h^2,6*a*d*f+6*c*d*f+7*d^2*f+7*d*f^2+6*d*f*g,8*b*c*d+8*a*e*f,8*b*d^2+9*d^2*e+10*a^2*g+a*e*g+5*d*e*g+4*e^2*g+3*e*g^2+2*e*g*h,10*a*c*d+10*c*f*g,8*d^2*e+10*c*g^2+2*b*c*h+3*c^2*h+5*c*d*h+9*d^2*h+c*g*h+4*c*h^2,8*d*e^2+8*b^2*f+9*d*e*h+9*b*f*h,3*a^2*b+4*a*b^2+a*b*c+10*a*c^2+5*a*b*d+9*b*d^2+2*a*b*e+8*d^2*h,8*b*c*f+8*d*g*h,9*b*e*f+8*e^2*f+9*b*d*h+8*d*h^2,9*b*f^2+8*e*f^2+4*b^2*g+b*c*g+10*c^2*g+5*b*f*g+3*b*g^2+2*b*g*h,10*a*c*f+10*a*d*g,10*c*d*g+10*a*f*g,8*b*f^2+10*a*g^2+3*a^2*h+2*a*e*h+5*a*f*h+9*f^2*h+a*g*h+4*a*h^2};
Ffirst = apply(16,i->(f0List#i)+q*(g1List#i));
Ifirst = ideal Ffirst;
