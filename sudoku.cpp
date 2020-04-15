#include <bits/stdc++.h>
using namespace std;

int n,m;

bool findUnassigned(vector<string> &A, int &row, int &col)
{
    for(row = 0;row<n;row++)
    {
        for(col = 0;col<m;col++)
        {
            if(A[row][col] == '.')
                return true;
        }
    }
    
    return false;
}


bool usedInRow(vector<string> &A, int row, char x)
{
    for(int i = 0;i<m;i++)
    {
        if(A[row][i] == x)
            return true;
    }
    
    return false;
}


bool usedInCol(vector<string> &A, int col, char x)
{
    for(int i = 0;i<n;i++)
    {
        if(A[i][col] == x)
            return true;
    }
    
    return false;
}


bool usedInBox(vector<string> &A,int row, int col, char x)
{
    for(int i = 0;i<3;i++)
    {
        for(int j = 0;j<3;j++)
        {
            if(A[row+i][col+j] == x)
                return true;
        }
    }
    
    return false;
}

bool isSafe(vector<string> &A, int &row, int &col, char num)
{
    if(!usedInRow(A, row, num) && 
        !usedInCol(A, col, num) &&
        !usedInBox(A, row - row%3, col - col%3, num) &&
        A[row][col] == '.')
        return true;
        
    return false;
}

bool solve(vector<string> &A)
{
    int row, col;
    if(!findUnassigned(A, row, col))
        return true;
        
    else
    {
        for(int i = 1;i<=9;i++)
        {
            string s = to_string(i);
            char num = s[0];
            if(A[row][col] == '.' && isSafe(A, row, col, num))
            {
                A[row][col] = num;
                
                if(solve(A))
                    return true;
                
                A[row][col] = '.';
            }
        }
    }
    
    return false;
}

void solveSudoku(vector<string> &A) 
{
    n = A.size();
    m = A[0].length();
    
    solve(A);
}

int main() {
	int t;
	cin>>t;
	while(t--)
	{
		vector<string> A;
		string s;
		for(int i = 0;i<9;i++)
		{
			cin>>s;
			A.push_back(s);
		}

		solveSudoku(A);

		for(int i = 0;i<9;i++)
		{
			for(int j = 0;j<9;j++)
				cout<<A[i][j]<<" ";

			cout<<endl;
		}
	}
}

