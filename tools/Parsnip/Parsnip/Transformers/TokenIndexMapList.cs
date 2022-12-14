using Microsoft.SqlServer.TransactSql.ScriptDom;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Parsnip.Transformers
{
    public class TokenIndexMapList
    {

        private List<TokenIndexMap> _tokenIndexMapList = new List<TokenIndexMap>();
        private int _nextIndex;
        private List<string> _nameList;

        //ctor- creates the tokenList based off of tree
        public TokenIndexMapList(TSqlFragment tree)
        {
            for (var i = tree.FirstTokenIndex; i <= tree.LastTokenIndex; i++)
            {
                _tokenIndexMapList.Add(new TokenIndexMap(i, tree.ScriptTokenStream[i].Text));
            }
            _nextIndex = _tokenIndexMapList.Count;
            _nameList = new List<string>();
        }
        public class TokenIndexMap
        {
            public int tokenIndex { get; set; }
            public string token { get; set; }
            public bool status { get; set; }// false is not in finalscript, true is in finalscript
            public TokenIndexMap(int tokenIndex, string token)
            {
                this.tokenIndex = tokenIndex;
                this.token = token;
                this.status = true;
            }
        }


        private int GetNextIndex()
        {

            _nextIndex++;
            return _nextIndex; 
        }

        public int GetTokenIndexPosition(int tokenIndex)
        {
            var xIndex = _tokenIndexMapList.FindIndex(n => n.tokenIndex == tokenIndex);
            return xIndex;
        }

        public string GetTokenOfIndex(int tokenIndex)
        {
            var x = _tokenIndexMapList.Find(item => item.tokenIndex == tokenIndex);
            return x.token;
        }

        public void Delete(int startTokenIndex, int endTokenIndex)
        {

            for (var i = startTokenIndex; i <= endTokenIndex; i++)
            {
                var removeIndex = GetTokenIndexPosition(i);
                _tokenIndexMapList[removeIndex].status = false;
                //_tokenIndexMapList.RemoveAt(removeIndex);
            }
            
        }

        public void Insert(int tokenIndex, string[] insertStatementArray)
        {
            var insertIndex = GetTokenIndexPosition(tokenIndex);
            int nextIndex;

           for(var i=insertStatementArray.Length-1; i>=0; i--) //issue with foreach inserting backwards -> think of another way?
            {
                nextIndex = GetNextIndex();
                _tokenIndexMapList.Insert(insertIndex, new TokenIndexMap(nextIndex, insertStatementArray[i]));
                insertIndex = GetTokenIndexPosition(nextIndex);
            }
            
        }

        public void Replace(int tokenIndex, string replaceToken)
        {
            var replaceTokenIndex = GetTokenIndexPosition(tokenIndex);  
            _tokenIndexMapList[replaceTokenIndex] = new TokenIndexMap(GetNextIndex(), replaceToken);
        }

        public void Select(int startTokenIndex, int endTokenIndex)
        {

            for (var i = startTokenIndex; i <= endTokenIndex; i++)
            {
                var selectIndex = GetTokenIndexPosition(i);
                _tokenIndexMapList[selectIndex].status = true;
            }

        }

        public List<string> GetUniqueNameList()
        {
            if (_nameList.Count() != 0)
            {
                _tokenIndexMapList.ForEach(token => token.status = false);
            }
            return _nameList.Select(item => item).Distinct().ToList<string>();
        }




        public List<string> ToStringList()
        {
            var finalList =  _tokenIndexMapList
                .Where(item => item.status == true)
                .Select( item => item.token)
                .ToList<String>();
            var namesList = GetUniqueNameList();
            finalList.AddRange(namesList);
            return finalList;

        }


    }
}
