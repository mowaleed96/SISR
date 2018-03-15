function [y] = MBHTM(u,m3,m4)

% GOAL
%  Transform a gaussian-distributed variable into a non-gaussian one,
%  given a target skewness (m3) and kurtosis (m4).

% INPUT
% u: random gaussian vector : size : [ 1 x N]
% m3: Target Skewness; is [1x1]
% m4: Target Kurtosis; is [1x1]

% OUTPUT
% y : Non gaussian variable with target m1,m2,m3 and m4. size : [ 1 x N]


%  example: [y]  = MBHTM(randn(1,1e5),0.5,4)



%% Reduction of the input
% variable used in input is reduced into a gaussian variable of variance equal to
% 1 and mean equal to 0:
m1 = nanmean(u);
m2 = nanvar(u);
u = (u-m1)/sqrt(m2) ;

% if the target skewness and kurtosis are the same as for a gaussian
% distribution, the output is the same as the input
if and(m3==0,m4 ==3),
    y = m1+sqrt(m2).*u;
    return
end

%% Test of applicability of the transformation
Ye = m4-3;% excess coefficient

test = (1/3.*(1-1.5.*Ye-sqrt(1+1.5*Ye))).^2.*(6./(sqrt(1+1.5*Ye)-1)-1);

if (m3^2> test||isnan(test)),
    fprintf(' applicability condition is not verified \n');
    fprintf([num2str(test,3),' < m3^2 = ',num2str(m3^2,2),' \n']);
    % the input is NaN;
    y = NaN(1,length(u));
    return
else
    fprintf('applicability condition is verified \n');
    fprintf([num2str(test,3),' >= m3^2 = ',num2str(m3^2,2),' \n']);
end


%% Main calculation

% guess of h3 and h4 before solving the system of equations_
h3_guess = m3./(4+2.*sqrt(1+1.5*Ye));
h4_guess = (sqrt(1+1.5*Ye)-1)./18;
guess = [h3_guess,h4_guess];

 % Call solver
options = optimoptions('fsolve','TolX',1e-10); % Option to display output
[x,~] = fsolve(@(x) myPolyFun(x,m3,m4),guess,options);

% get h3 and h4
h3=x(1);
h4=x(2);

% get a,b and alpha
a = h3/(3*h4);
b = 1/(3*h4);
alpha = 1./(sqrt(1+2*h3^2+6*h4.^2));

% get the non gaussian variable y
y = alpha./b.*(u.^3/3+a.*u.^2+(b-1).*u-a);

y = m1+sqrt(m2).*y;

    function F = myPolyFun(x,Y3,Y4)
        
        F= [-Y3+(2.*x(1).*(3+4.*x(1).^2+18.*x(2)+54.*x(2).^2))./(sqrt(1+2*x(1).^2+6*x(2).^2)).^3;
            -Y4+3.*(1+20.*x(1).^4+8.*x(2)+84.*x(2).^2+432.*x(2).^3 +1116.*x(2).^4+(4.*x(1).^2.*(5+48.*x(2)+168.*x(2).^2)))./...
            (1+2*x(1).^2+6*x(2).^2).^2];
    end
end

