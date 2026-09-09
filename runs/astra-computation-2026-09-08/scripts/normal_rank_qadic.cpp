/* Exact finite-precision normal rank. No CAS or external libraries.
 * Build only in the root agent's exclusive computation slot:
 *   c++ -O3 -std=c++17 normal_rank_qadic.cpp -o normal_rank_qadic
 * Run: normal_rank_qadic INPUT.bin OUTPUT_PREFIX
 *
 * This uses the 1555-edge constant spanning forest prepared by Python,
 * differentiates L(z)-P0 W-M(z)W=0, and forms only a5405x109 Schur matrix.
 * At each q-adic step, unit elimination preserves precision; division of
 * the entire active matrix by q^v decreases available precision by v.
 * Only rank LOWER bounds, hence normal/Hodge UPPER bounds, are certified.
 */
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

using U=uint32_t;
using I=int32_t;
using L=int64_t;
namespace fs=std::filesystem;
static void require(bool ok,const std::string& s){if(!ok)throw std::runtime_error(s);}
static U prime;
static U mod(L x){x%=prime;if(x<0)x+=prime;return U(x);}
static U power(U a,U n){U r=1;while(n){if(n&1)r=U(uint64_t(r)*a%prime);a=U(uint64_t(a)*a%prime);n>>=1;}return r;}
template<class T> static std::vector<T> readv(std::ifstream& f,size_t n){
    std::vector<T> v(n);f.read(reinterpret_cast<char*>(v.data()),n*sizeof(T));require(bool(f),"truncated binary input");return v;
}
static void immutable(const std::string& path,const char* bytes,size_t n){
    if(fs::exists(path)){
        std::ifstream in(path,std::ios::binary);std::vector<char> old((std::istreambuf_iterator<char>(in)),{});
        require(old.size()==n&&std::equal(old.begin(),old.end(),bytes),"existing output differs: "+path);return;
    }
    std::ofstream out(path,std::ios::binary);require(bool(out),"cannot create output: "+path);out.write(bytes,n);require(bool(out),"output write failed");
}
static void save_schur(const std::string& path,U order,U nr,U nc,const std::vector<U>& a){
    std::vector<char> out(8+5*sizeof(U)+(size_t(order)+1)*nr*nc*sizeof(U));
    const char magic[]="GSSCHUR1";std::copy(magic,magic+8,out.begin());
    U h[5]={prime,order,nr,nc,1};std::copy(reinterpret_cast<char*>(h),reinterpret_cast<char*>(h)+sizeof(h),out.begin()+8);
    std::copy(reinterpret_cast<const char*>(a.data()),reinterpret_cast<const char*>(a.data())+(size_t(order)+1)*nr*nc*sizeof(U),out.begin()+8+sizeof(h));
    immutable(path,out.data(),out.size());
}

int main(int argc,char** argv){try{
    require(argc==3,"usage: normal_rank_qadic INPUT.bin OUTPUT_PREFIX");
    const std::string input=argv[1],prefix=argv[2];
    require(fs::exists(fs::path(prefix).parent_path()),"output parent must already exist");
    const auto started=std::chrono::steady_clock::now();
    auto elapsed=[&](){return std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();};
    std::ifstream in(input,std::ios::binary);require(bool(in),"cannot open input");
    auto magic=readv<char>(in,8);require(std::string(magic.begin(),magic.end())=="GSNRANK1","wrong input magic");
    auto h=readv<U>(in,10);prime=h[0];const U N=h[1],NZ=h[2],K=h[3],R=h[4],TOP=h[5],BOT=h[6],NT=h[7],NR=h[8],NE=h[9];
    require(prime==101&&N>=1&&N<=6&&NZ==1664&&K==109&&R==9900&&TOP==2940&&BOT==6960&&NT==1555&&NR==5405&&NE==10192,"unexpected dimensions");
    auto linear=readv<I>(in,R*4);auto tree=readv<I>(in,NT*4);auto anchors=readv<I>(in,K);
    auto component=readv<I>(in,NZ);auto remaining=readv<I>(in,NR);auto edges=readv<I>(in,NE*3);
    auto zb=readv<U>(in,(N+1)*NZ);auto wb=readv<U>(in,(N+1)*TOP);
    require(in.peek()==EOF,"unexpected trailing binary data");
    for(U x:zb)require(x<prime,"noncanonical base z residue");for(U x:wb)require(x<prime,"noncanonical base W residue");
    // Independently check the base incidence identity to all supplied orders.
    for(U n=0;n<=N;n++){
        std::vector<L> cross(R,0);
        for(U d=1;d<n;d++)for(U e=0;e<NE;e++){
            U r=edges[3*e],c=edges[3*e+1],v=edges[3*e+2],a=zb[d*NZ+v];if(!a)continue;
            for(U j=0;j<30;j++)cross[r*30+j]+=L(a)*wb[(n-d)*TOP+c*30+j];
        }
        for(U r=0;r<R;r++){
            L x=0;for(U j=0;j<2;j++){I v=linear[4*r+j];if(v>=0)x+=L(linear[4*r+2+j])*zb[n*NZ+v];}
            if(r<TOP)x-=wb[n*TOP+r];
            require(mod(x-cross[r])==0,"input base incidence identity fails at order "+std::to_string(n)+" row "+std::to_string(r));
        }
        std::cout<<"BASE_INCIDENCE_ORDER "<<n<<" ZERO\n"<<std::flush;
    }
    // Variation matrices have109 columns, one for each constant kernel class.
    std::vector<U> zv(size_t(N+1)*NZ*K,0),wv(size_t(N+1)*TOP*K,0),schur(size_t(N+1)*NR*K,0);
    auto Z=[&](U n,U v,U k)->U&{return zv[(size_t(n)*NZ+v)*K+k];};
    auto W=[&](U n,U r,U k)->U&{return wv[(size_t(n)*TOP+r)*K+k];};
    for(U v=0;v<NZ;v++)if(component[v]>=0)Z(0,v,component[v])=1;
    std::vector<bool> kept(BOT,false);for(I r:remaining)kept[r]=true;
    for(U n=0;n<=N;n++){
        std::vector<L> cross(size_t(R)*K,0);
        // M(z_i) delta W_(n-i), i>=1.
        for(U d=1;d<=n;d++)for(U e=0;e<NE;e++){
            U r=edges[3*e],c=edges[3*e+1],v=edges[3*e+2],a=zb[d*NZ+v];if(!a)continue;
            for(U j=0;j<30;j++){
                L* dest=&cross[(size_t(r)*30+j)*K];const U* source=&W(n-d,c*30+j,0);
                for(U k=0;k<K;k++)dest[k]+=L(a)*source[k];
            }
        }
        // M(delta z_i) W_(n-i), i<n, since W_0=0.
        for(U d=0;d<n;d++)for(U e=0;e<NE;e++){
            U r=edges[3*e],c=edges[3*e+1],v=edges[3*e+2];const U* source=&Z(d,v,0);
            for(U j=0;j<30;j++){
                U b=wb[(n-d)*TOP+c*30+j];if(!b)continue;
                L* dest=&cross[(size_t(r)*30+j)*K];
                for(U k=0;k<K;k++)dest[k]+=L(b)*source[k];
            }
        }
        if(n){
            // Free coordinates at positive order are zero; the tree solves
            // every selected bottom equation in O(1555*109) scalar steps.
            for(U e=0;e<NT;e++){
                U child=tree[4*e],parent=tree[4*e+1],row=tree[4*e+2];I sign=tree[4*e+3];
                for(U k=0;k<K;k++)Z(n,child,k)=mod((parent==NZ?0:L(Z(n,parent,k)))+L(sign)*cross[(size_t(TOP)+row)*K+k]);
            }
        }
        std::vector<U> residual(size_t(R)*K,0);
        for(U r=0;r<R;r++)for(U k=0;k<K;k++){
            L x=-cross[size_t(r)*K+k];
            for(U j=0;j<2;j++){I v=linear[4*r+j];if(v>=0)x+=L(linear[4*r+2+j])*Z(n,v,k);}
            residual[size_t(r)*K+k]=mod(x);
        }
        for(U r=0;r<TOP;r++)for(U k=0;k<K;k++)W(n,r,k)=residual[size_t(r)*K+k];
        for(U r=0;r<BOT;r++)if(!kept[r])for(U k=0;k<K;k++)require(residual[size_t(TOP+r)*K+k]==0,"forest solve failed");
        for(U r=0;r<NR;r++)for(U k=0;k<K;k++)schur[(size_t(n)*NR+r)*K+k]=residual[size_t(TOP+remaining[r])*K+k];
        if(n==0)require(std::all_of(schur.begin(),schur.begin()+size_t(NR)*K,[](U x){return x==0;}),"constant Schur matrix is nonzero");
        save_schur(prefix+"_schur_order"+std::to_string(n)+".bin",n,NR,K,schur);
        std::cout<<"NORMAL_SCHUR_ORDER "<<n<<" COMPLETE seconds "<<elapsed()<<"\n"<<std::flush;
    }
    // All rank work below acts on the small109-column Schur matrix.
    auto A=[&](U d,U r,U c)->U&{return schur[(size_t(d)*NR+r)*K+c];};
    std::vector<I> rowlabels=remaining,collabels=anchors;
    U rank=0,precision=N+1,offset=0,total_valuation=0,leading_coefficient=1;
    struct Pivot{I row,col;U valuation,unit,precision;};std::vector<Pivot> certificates;
    while(rank<K&&rank<NR&&precision){
        U ri=NR,ci=K;
        for(U r=rank;r<NR&&ri==NR;r++)for(U c=rank;c<K;c++)if(A(0,r,c)){ri=r;ci=c;break;}
        if(ri==NR){
            U first=precision;
            for(U d=1;d<precision&&first==precision;d++)for(U r=rank;r<NR&&first==precision;r++)for(U c=rank;c<K;c++)if(A(d,r,c)){first=d;break;}
            if(first==precision){
                std::cout<<"REMAINING_SCHUR_ZERO_TO_AVAILABLE_PRECISION "<<precision<<"; NOT_ALL_ORDERS_ZERO\n"<<std::flush;break;
            }
            for(U d=0;d<precision-first;d++)for(U r=rank;r<NR;r++)for(U c=rank;c<K;c++)A(d,r,c)=A(d+first,r,c);
            precision-=first;offset+=first;
            std::cout<<"DIVIDE_ACTIVE_MATRIX_BY_Q_POWER "<<first<<" REMAINING_PRECISION "<<precision<<"\n"<<std::flush;
            continue;
        }
        if(ri!=rank){for(U d=0;d<precision;d++)for(U c=rank;c<K;c++)std::swap(A(d,rank,c),A(d,ri,c));std::swap(rowlabels[rank],rowlabels[ri]);}
        if(ci!=rank){for(U d=0;d<precision;d++)for(U r=rank;r<NR;r++)std::swap(A(d,r,rank),A(d,r,ci));std::swap(collabels[rank],collabels[ci]);}
        U unit=A(0,rank,rank);require(unit!=0,"nonunit q-adic pivot");
        certificates.push_back({rowlabels[rank],collabels[rank],offset,unit,precision});
        total_valuation+=offset;leading_coefficient=U(uint64_t(leading_coefficient)*unit%prime);
        std::vector<U> inv(precision,0);inv[0]=power(unit,prime-2);
        for(U d=1;d<precision;d++){L sum=0;for(U j=1;j<=d;j++)sum+=L(A(j,rank,rank))*inv[d-j];inv[d]=mod(-L(inv[0])*sum);}
        std::vector<U> prow(size_t(K)*precision,0);
        for(U c=rank;c<K;c++)for(U d=0;d<precision;d++){
            L sum=0;for(U j=0;j<=d;j++)sum+=L(A(j,rank,c))*inv[d-j];prow[size_t(c)*precision+d]=mod(sum);
        }
        for(U c=rank;c<K;c++)for(U d=0;d<precision;d++)A(d,rank,c)=prow[size_t(c)*precision+d];
        require(A(0,rank,rank)==1,"pivot normalization failed");
        for(U d=1;d<precision;d++)require(A(d,rank,rank)==0,"pivot inverse precision failure");
        for(U r=rank+1;r<NR;r++){
            std::vector<U> factor(precision);bool nonzero=false;
            for(U d=0;d<precision;d++){factor[d]=A(d,r,rank);nonzero|=factor[d]!=0;}
            if(!nonzero)continue;
            for(U c=rank+1;c<K;c++)for(U d=0;d<precision;d++){
                L sum=0;for(U j=0;j<=d;j++)sum+=L(factor[j])*prow[size_t(c)*precision+d-j];A(d,r,c)=mod(L(A(d,r,c))-sum);
            }
            for(U d=0;d<precision;d++)A(d,r,rank)=0;
        }
        rank++;
        std::cout<<"CERTIFIED_ADDITIONAL_PIVOT "<<rank<<" VALUATION "<<offset<<" UNIT "<<unit<<" PRECISION "<<precision<<" seconds "<<elapsed()<<"\n"<<std::flush;
    }
    require(rank<=46,"rank contradicts the intended characteristic-zero h0(N)>=63; investigate inputs/implementation");
    std::string json="{\n  \"status\":\"COMPUTER-CERTIFIED finite-precision rank lower bound; Hodge upper bound conditional on the accepted integral smoothing bridge\",\n";
    json+="  \"prime\":"+std::to_string(prime)+",\n  \"input_order\":"+std::to_string(N)+",\n";
    json+="  \"constant_rank\":1555,\n  \"additional_rank_lower_bound\":"+std::to_string(rank)+",\n";
    json+="  \"full_normal_map_rank_lower_bound\":"+std::to_string(1555+rank)+",\n";
    json+="  \"h0_normal_upper_bound\":"+std::to_string(109-rank)+",\n  \"h21_upper_bound\":"+std::to_string(46-rank)+",\n";
    json+="  \"schur_minor_valuation\":"+std::to_string(total_valuation)+",\n  \"schur_minor_leading_coefficient_mod101\":"+std::to_string(leading_coefficient)+",\n";
    json+="  \"available_active_precision\":"+std::to_string(precision)+",\n  \"all_orders_vanishing_claimed\":false,\n  \"rank_equality_claimed\":false,\n  \"pivots\":[\n";
    for(size_t i=0;i<certificates.size();i++){
        auto x=certificates[i];json+="    {\"original_bottom_row\":"+std::to_string(x.row)+",\"original_free_coordinate_anchor\":"+std::to_string(x.col)+",\"q_valuation\":"+std::to_string(x.valuation)+",\"unit\":"+std::to_string(x.unit)+",\"available_precision\":"+std::to_string(x.precision)+"}"+(i+1<certificates.size()?",\n":"\n");
    }
    json+="  ],\n  \"elapsed_seconds\":"+std::to_string(elapsed())+"\n}\n";
    immutable(prefix+"_rank_certificate.json",json.data(),json.size());
    std::cout<<"COMPUTER_CERTIFIED_H0N_UPPER_BOUND "<<109-rank<<" H21_UPPER_BOUND "<<46-rank<<"; NO_EQUALITY_CLAIM\n";
    std::cout<<"CERTIFICATE "<<prefix<<"_rank_certificate.json\n";return 0;
}catch(const std::exception& e){std::cerr<<"FAILED_OR_UNFINISHED: "<<e.what()<<"\n";return 2;}}
